.PHONY: all
all:
	poetry install
	poetry run pyinstaller --onefile src/kapply.py
