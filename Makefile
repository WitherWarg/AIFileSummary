main:
	@KEY=$$(cat key.txt); export GEMINI_API_KEY="$$KEY"; python3 main.py