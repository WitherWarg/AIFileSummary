from google.genai import Client as AIAgent
from pathlib import Path
from aspose.words import Document
from os import remove, rmdir
from logger import logger
from re import search
from os.path import exists

def load_files(ai_agent: AIAgent, folder_path: str) -> list:
    folder = Path(folder_path)
    files = []

    logger.info("Loading files:")
    logger.info("\tConversion of Word Documents to PDF files...")
    logger.info("\tUpload of PDF files to AI Agent...")

    for file in folder.rglob('*'):
        if file.is_file() and file.name != ".DS_Store":
            output_path = str(file).replace(".docx", ".pdf", 1).replace(folder_path, folder_path+"Copy", 1)

            document = Document(str(file))
            document.save(output_path)

            logger.info(f"\tConverted {file.name} to {file.name.replace('.docx', '.pdf', 1)}.")

            files.append(ai_agent.files.upload(file=output_path))

            logger.info(f"\tUploaded {file.name.replace('.docx', '.pdf', 1)} to AI Agent.")

    logger.info("Loading complete.\n")

    return files

def delete_files(folder_path: str):
    logger.info("Cleanup:")
    logger.info("\tDeleting files...")

    folder = Path(folder_path + "Copy")
    for file in folder.rglob('*'):
        if file.is_file():
            remove(str(file))
            logger.info(f"\tDeleted {file.name}.")

    rmdir(folder_path + "Copy")

    logger.info(f"Cleanup complete.\n")

def get_unique_filename(filename: str):
    counter = 1
    while exists(filename):
        filename = f"{filename}{counter}.txt"
        counter += 1
    return filename

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
            You are and advisor on a set of files I, the developer, has
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
            
            filename = get_unique_filename(search(r"\b\S+\.txt\b", response).group())

            with open(filename, "w") as output_file:
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

    files = load_files(ai_agent, folder_path)
    prompt_user(ai_agent, "gemini-2.5-pro", files)
    delete_files(folder_path)

    logger.info("Program closed.")

if __name__ == "__main__":
    main()