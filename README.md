# AI File Summarizer

This project uses Google's Gemini AI to scan and summarizes a list of reports made by a company.

## Requirements

- Python 3.7 or higher
- `git`
- `pip` (comes with Python)

## Installation

Follow these steps to set up the project locally.

### 1. Clone the repository

```bash
git clone git@github.com:WitherWarg/AIFileSummary.git
cd AIFileSummary
```

### 2. Create a virtual environment

This is for those who want to prevent installing packages that interfere with other projects on their system.

```bash
python -m venv venv
```

#### MacOs/Linux

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

To run the program:

```bash
python main.py
```

## Notes

If you encounter permission or dependency issues, try upgrading pip:

```bash
pip install --upgrade pip
```
