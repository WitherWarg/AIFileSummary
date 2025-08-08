run:
	@KEY=$$(cat key.txt); export GEMINI_API_KEY="$$KEY"; python3 main.py

clean:
	@FILES=$$(find . -maxdepth 1 -type f -name "*.txt" ! -name "requirements.txt" ! -name "key.txt" | sed 's|^\./||'); \
	DIRS=$$(find . -type d -name "*Copy" | sed 's|^\./||'); \
	if [ -z "$$FILES" ] && [ -z "$$DIRS" ]; then \
		echo "No matching files or directories found to delete."; \
		exit 0; \
	fi; \
	if [ -n "$$FILES" ]; then \
		echo "The following files will be deleted:"; \
		echo "$$FILES"; \
	fi; \
	if [ -n "$$DIRS" ]; then \
		echo "The following directories will be deleted:"; \
		echo "$$DIRS"; \
	fi; \
	read -p "Are you sure you want to delete these? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "Deleting..."; \
		echo "$$FILES" | xargs -r rm -f; \
		echo "$$DIRS" | xargs -r rm -rf; \
	else \
		echo "Aborted."; \
	fi

dependencies:
	@pip freeze > requirements.txt