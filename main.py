from google.genai import Client
from pathlib import Path

client = Client()
model = "gemini-2.5-pro"

folder_path = "./Sample"
folder = Path(folder_path)
files = []

for file in folder.rglob('*'):
    if file.is_file():
        files.append(str(file))
        files.append(client.files.upload(file=str(file)))

while True:
    try:
        prompt = input("Prompt: ")
    except KeyboardInterrupt:
        print()
        break

    contents = [
        prompt,
        '''
        The user will ask you questions about the contents of these files.
        You will summarize the contents and ONLY the contents relating to
        the user's query in two to three sentences. Do not use transition
        terms such as "Based on the report" or "According to the projet".
        Instead, get right into the subject right away.
        '''
    ]
    contents.extend(files)
    print(contents)

    # print(client.models.generate_content(model=model, contents=contents).text)