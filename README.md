# pdf-merger

## How to Use

This tool merges multiple PDF files based on a filename regex pattern.

### Basic usage

```sh
python pdf_merger.py -p "<PATTERN>" -o <OUTPUT.pdf>
```

- `-p, --pattern` — **Required.** Regex pattern to match target PDF filenames (e.g., `L\d.*\.pdf`).
- `-o, --output` — **Required.** Name for the merged PDF file (e.g., `merged.pdf`).
- `-d, --directory` — _(Optional)_ Directory to search for PDFs. Defaults to the current directory.

### Examples

Merge all PDFs starting with `L` followed by a digit:

```sh
python pdf_merger.py -p "L\d.*\.pdf" -o merged_lectures.pdf
```

Merge all PDFs NOT starting with `L`:

```sh
python pdf_merger.py -p '^(?!L).*\.pdf' -o merged_others.pdf
```

Merge all PDF files in the folder:

```sh
python pdf_merger.py -p ".*\.pdf" -o all_files.pdf
```

Change the directory being searched:

```sh
python pdf_merger.py -p "^L.*\.pdf" -o lectures.pdf -d ./lectures_folder
```

> **Note**:
>
> - Regex patterns are _case-sensitive_ unless you use a pattern to ignore case.
> - Single quotes are recommended for regex patterns with special characters on Unix shells.

### Installation

Requirements (see `requirements.txt`):

- Python 3.6+
- `pypdf` (or `PyPDF2`)
- `argparse` (for Python <3.2)
- `pathlib` (for Python <3.4)

Install dependencies via pip:

```sh
pip install -r requirements.txt
```

### Output

- The script prints which PDFs will be merged.
- The output file will have `.pdf` appended if not provided.
- The tool will list warnings for unreadable or malformed PDFs but continue processing remaining files.
