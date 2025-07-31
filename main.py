from google.genai import Client
from pathlib import Path
from aspose.words import Document
from os import system
from time import sleep
from math import floor
from shutil import rmtree

def load_files(client: Client, folder_path: str):
    PROGRESS_BAR_LENGTH = 10
    BORDER_CHAR = "|"
    EMPTY_CHAR = " "
    FULL_CHAR = "*"

    folder = Path(folder_path)
    files = []
    number_of_files = 0

    for file in folder.rglob('*'):
        if file.is_file and file.name != ".DS_Store":
            number_of_files += 1

    i = 0
    print(BORDER_CHAR + PROGRESS_BAR_LENGTH * EMPTY_CHAR + BORDER_CHAR)
    for file in folder.rglob('*'):
        if file.is_file() and file.name != ".DS_Store":
            output_path = str(file).replace(".docx", ".pdf", 1).replace(folder_path, folder_path+"Copy", 1)

            document = Document(str(file))
            document.save(output_path)

            files.append(client.files.upload(file=output_path))

            system('clear')
            i += 1
            progress = floor(i / number_of_files * PROGRESS_BAR_LENGTH)
            print(BORDER_CHAR + progress * FULL_CHAR + (PROGRESS_BAR_LENGTH-progress) * EMPTY_CHAR + BORDER_CHAR)

    print("DOWNLOAD COMPLETE")
    sleep(1.5)
    system('clear')

    return files

def delete_files(folder_path: str):
    rmtree(folder_path + "Copy")

def prompt_user(client: Client, model: str, files: list):
    while True:
        prompt = input("Prompt [Press Q to Quit]: ")
        if prompt.upper() == "Q":
            return

        contents = [
            prompt,
            """
            You are and advisor on a set of files I, the developer, has
            provided. The user will ask you questions about the contents
            of these files. You will summarize the contents and ONLY the
            contents relating to the user's query in two to three
            sentences. Do not use transition terms such as "Based on the
            report" or "According to the projet". Instead, get right into
            the subject matter.
            """
        ]
        contents.extend(files)

        print(client.models.generate_content(model=model, contents=contents).text)

def main():
    system('clear')

    client = Client()
    model = "gemini-2.0-flash"

    folder_path = "/Users/yuftenkhemiss/Documents/Optimiz/AIFileSummary/Sample"

    files = load_files(client, folder_path)
    prompt_user(client, model, files)
    delete_files(folder_path)

if __name__ == "__main__":
    main()