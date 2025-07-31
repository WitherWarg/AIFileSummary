from google import genai

def generate_prompt(contents):
    return genai.Client().models.generate_content(
        model="gemini-2.5-flash", contents=contents
    ).text