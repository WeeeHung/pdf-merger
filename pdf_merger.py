#!/usr/bin/env python3
r"""
PDF Merger with Regex Pattern Matching

This script merges PDF files based on regex patterns and allows you to specify
the output filename.

Usage examples:
    # Merge all files starting with "L" followed by a digit
    python pdf_merger.py -p "L\d.*\.pdf" -o merged_lectures.pdf
    
    # Merge all files NOT starting with "L" (use single quotes for patterns with !)
    python pdf_merger.py -p '^(?!L).*\.pdf' -o merged_others.pdf
    
    # Merge all PDF files
    python pdf_merger.py -p ".*\.pdf" -o all_files.pdf
"""

import re
import os
import sys
import argparse
from pathlib import Path
from typing import List

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfWriter, PdfReader
    except ImportError:
        print("Error: pypdf or PyPDF2 is required. Install it with: pip install pypdf")
        sys.exit(1)


def natural_sort_key(text: str) -> tuple:
    """Generate a key for natural sorting (handles numbers correctly)."""
    def convert(text_part):
        return int(text_part) if text_part.isdigit() else text_part.lower()
    
    return [convert(c) for c in re.split(r'(\d+)', text)]


def find_matching_pdfs(directory: Path, pattern: str) -> List[Path]:
    """
    Find all PDF files in the directory that match the regex pattern.
    
    Args:
        directory: Directory to search in
        pattern: Regex pattern to match against filenames
        
    Returns:
        List of matching PDF file paths, sorted naturally
    """
    try:
        regex = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        print(f"Error: Invalid regex pattern: {e}")
        sys.exit(1)
    
    matching_files = []
    
    for file_path in directory.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.pdf':
            filename = file_path.name
            if regex.search(filename):
                matching_files.append(file_path)
    
    # Sort naturally (L2 comes before L10)
    matching_files.sort(key=lambda x: natural_sort_key(x.name))
    
    return matching_files


def merge_pdfs(pdf_files: List[Path], output_path: Path) -> None:
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        pdf_files: List of PDF file paths to merge
        output_path: Path for the output merged PDF
    """
    if not pdf_files:
        print("No PDF files found matching the pattern.")
        return
    
    print(f"\nFound {len(pdf_files)} PDF file(s) to merge:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf_file.name}")
    
    print(f"\nMerging PDFs into: {output_path.name}")
    
    writer = PdfWriter()
    
    for pdf_file in pdf_files:
        try:
            print(f"  Processing: {pdf_file.name}")
            reader = PdfReader(str(pdf_file))
            
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])
                
        except Exception as e:
            print(f"  Warning: Failed to process {pdf_file.name}: {e}")
            continue
    
    # Write the merged PDF
    try:
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        print(f"\n✓ Successfully merged {len(pdf_files)} PDF(s) into: {output_path}")
        print(f"  Output size: {output_path.stat().st_size / (1024*1024):.2f} MB")
    except Exception as e:
        print(f"\n✗ Error writing output file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Merge PDF files based on regex patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge all files starting with "L" followed by a digit
  python pdf_merger.py -p "L\\d.*\\.pdf" -o merged_lectures.pdf
  
  # Merge all files NOT starting with "L" (use single quotes for patterns with !)
  python pdf_merger.py -p '^(?!L).*\\.pdf' -o merged_others.pdf
  
  # Merge all PDF files
  python pdf_merger.py -p ".*\\.pdf" -o all_files.pdf
  
  # Simple pattern: files starting with "L"
  python pdf_merger.py -p "^L.*\\.pdf" -o lectures.pdf
        """
    )
    
    parser.add_argument(
        '-p', '--pattern',
        type=str,
        required=True,
        help='Regex pattern to match PDF filenames (e.g., "L\\d.*\\.pdf" for files starting with L and a digit)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Output filename for the merged PDF'
    )
    
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='Directory to search for PDF files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Convert to Path objects
    directory = Path(args.directory).resolve()
    output_path = Path(args.output)
    
    # Validate directory
    if not directory.exists() or not directory.is_dir():
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        sys.exit(1)
    
    # Ensure output filename has .pdf extension
    if output_path.suffix.lower() != '.pdf':
        output_path = output_path.with_suffix('.pdf')
    
    # If output is not absolute, make it relative to the directory
    if not output_path.is_absolute():
        output_path = directory / output_path
    
    # Find matching PDFs
    print(f"Searching for PDFs matching pattern: {args.pattern}")
    print(f"Directory: {directory}")
    
    matching_pdfs = find_matching_pdfs(directory, args.pattern)
    
    # Merge PDFs
    merge_pdfs(matching_pdfs, output_path)


if __name__ == '__main__':
    main()
