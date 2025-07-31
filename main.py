from google.genai import Client as AIAgent
from pathlib import Path
from aspose.words import Document
from time import sleep
from os import remove, rmdir
from logger import logger

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
    sleep(1.5)

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
    sleep(1.5)

def prompt_user(ai_agent: AIAgent, model: str, files: list):
    logger.info("Initiating AI agent discussion:")
    while True:
        logger.info("\tPrompting user.")
        prompt = input("Prompt [Press Q to Quit]: ")
        if prompt.upper() == "Q":
            break

        logger.info("\tGenerating response...")
        contents = [
            prompt,
            """
            You are and advisor on a set of files I, the developer, has
            provided. The user will ask you questions about the contents
            of these files. You will summarize the contents and ONLY the
            contents relating to the user's query in two to three
            sentences, unless the user requests a longer answer. Do not
            use transition terms such as "Based on the report" or "According
            to the projet". Instead, get right into the subject matter.
            """
        ]
        contents.extend(files)

        print(ai_agent.models.generate_content(model=model, contents=contents).text)
        logger.info("\tResponse generated.")
    logger.info("AI Agent discussion terminated\n")
    sleep(1.5)

def main():
    ai_agent = AIAgent()
    model = "gemini-2.0-flash"

    folder_path = "/Users/yuftenkhemiss/Documents/Optimiz/AIFileSummary/Sample"

    files = load_files(ai_agent, folder_path)
    prompt_user(ai_agent, model, files)
    delete_files(folder_path)

    logger.info("Program closed.")

if __name__ == "__main__":
    main()