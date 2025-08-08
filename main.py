from google.genai import Client as AIAgent
from pathlib import Path
from aspose.words import Document
from os import remove
from logger import logger
from re import search
from os.path import exists, splitext
from shutil import rmtree
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from math import ceil
import time

def get_all_files(folder_path: str):
    for file in Path(folder_path).rglob('*'):
        if file.is_file() and file.name != ".DS_Store":
            yield file

def process_file(file: Path, ai_agent: AIAgent, folder_path: str, files: list, lock: Lock):
    output_path = str(file).replace(".docx", ".pdf", 1).replace(folder_path, folder_path + "Copy", 1)

    document = Document(str(file))
    document.save(output_path)

    logger.info(f"\tConverted {file.name} to {file.name.replace('.docx', '.pdf', 1)}.")

    uploaded_file = ai_agent.files.upload(file=output_path)

    with lock:
        files.append(uploaded_file)

    logger.info(f"\tUploaded {file.name.replace('.docx', '.pdf', 1)} to AI Agent.")

def load_files(ai_agent: AIAgent, folder_path: str, max_threads: int = 50, files_per_thread: int = 4) -> list:
    logger.info("Loading files:")

    copy_folder = Path(folder_path + "Copy")
    copy_folder.mkdir(parents=True, exist_ok=True)

    files = []
    lock = Lock()

    all_files = list(get_all_files(folder_path))
    num_files = len(all_files)

    max_workers = max(1, min(max_threads, ceil(num_files / files_per_thread)))

    logger.info(f"Using {max_workers} threads for processing {num_files} files.")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, file, ai_agent, folder_path, files, lock) for file in all_files]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error processing file: {e}")

    logger.info("Loading complete.\n")

    return files

def delete_files(folder_path: str):
    logger.info("Cleanup:")
    logger.info("\tDeleting generated folder...")

    copy_folder = Path(folder_path + "Copy")
    if copy_folder.exists():
        rmtree(copy_folder)
        logger.info(f"\tDeleted folder and all contents: {copy_folder}")
    else:
        logger.info(f"\tFolder not found: {copy_folder}")

    logger.info("Cleanup complete.\n")

def get_unique_filename(filename: str):
    root_name, file_type = splitext(filename)
    if file_type.lower() != ".txt":
        raise ValueError("Filename must end with .txt")

    counter = 1
    new_filename = filename

    while exists(new_filename):
        new_filename = f"{root_name}{counter}{file_type}"
        counter += 1

    return new_filename

def prompt_user(ai_agent: AIAgent, model: str, files: list):
    logger.info("Beginning AI agent discussion:")

    conversation_history = []

    EXPORT_PREFIX_FORMAT = r"Response must be exported.\nFile name: [Insert File Name Here].txt\n"
    EXPORT_PREFIX = "Response must be exported.\nFile name: "

    while True:
        logger.info("\tPrompting user.")
        prompt = input("Prompt [Press Q to Quit]: ")
        if prompt.upper() == "Q":
            break

        logger.info("\tGenerating response...")
        contents = [
            f"""
            You are an advisor on a set of files I, the developer, have
            provided. If it exists, past conversation history with the
            user will be provided. The user will ask you questions about
            the contents of these files. You will summarize the contents
            and ONLY the contents relating to the user's query. Do not
            use transition terms such as "Based on the report" or
            "According to the project". Instead, get right into the
            subject matter. If the user asks you to export your response
            as a file, YOU MUST begin your response with the following text:
            "{EXPORT_PREFIX_FORMAT}". Format it as a raw text file and make.
            """,
            prompt
        ]
        contents.extend(files)
        contents.extend(conversation_history)

        response = ai_agent.models.generate_content(model=model, contents=contents).text

        conversation_history.append(prompt)
        conversation_history.append(response)

        if response.startswith(EXPORT_PREFIX):
            logger.info("\tExporting file...")
            response = response.removeprefix(EXPORT_PREFIX)

            match = search(r"\b\S+\.txt\b", response)
            if not match:
                logger.error("Export requested but filename not found in response.")
                print("Error: Export filename not found.")
                continue

            filename = get_unique_filename(match.group())

            with open(filename, "w", encoding="utf-8") as output_file:
                output_file.write(response.removeprefix(filename + '\n'))

            logger.info("\tExporting complete.")
            print(f"Response has been exported to {filename}.")
        else:
            print(response)
            logger.info("\tResponse generated.")

    logger.info("AI Agent discussion has ended.\n")

def main():
    ai_agent = AIAgent()

    folder_path = "/Users/yuftenkhemiss/Documents/Optimiz/AIFileSummary/Sample"

    start = time.perf_counter()

    files = load_files(ai_agent, folder_path, max_threads=50, files_per_thread=1)

    end = time.perf_counter()

    logger.info(f"File loading time: {end - start:.6f} seconds")

    prompt_user(ai_agent, model="gemini-2.5-pro", files=files)
    delete_files(folder_path)

    logger.info("Program closed.")

if __name__ == "__main__":
    main()