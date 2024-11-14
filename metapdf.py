"""
METAPDF is a programm that automatically reads out the metadata of a single or multiple PDF files
and saves it in a .csv file.
"""

import argparse
import os
import csv
from PyPDF2 import PdfReader
from typing import List, Optional, Dict


def ensure_csv_extension(outputfile_name: str) -> str:
    """
    Checks if the outputfile name (input command -n) has a .csv extension and adds it if missing.

    Args:
        outputfile_name (str): The file name to check.

    Returns:
        str: The outputfile name with .csv extension if it was missing.
    """
    if not outputfile_name.lower().endswith('.csv'):
        outputfile_name += '.csv'
    return outputfile_name


def extract_pdf_version(pdf_path: str) -> str:
    """
    Extracts the PDF version from the PDF header.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The PDF version (e.g., '1.4') or 'unknown' if not detected.
    """
    with open(pdf_path, 'rb') as f:
        # reads the first bites of the file to determin the version
        # the first 8 bites includes the version number, e.g.: "%PDF-1.4"
        header = f.read(8).decode('utf-8')
        if header.startswith('%PDF-'):
            return header[5:].strip()
        return 'unknown'


def extract_metadata(pdf_path: str) -> Optional[Dict[str, str]]:
    """
    Extracts metadata from a single PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing metadata such as Title, Author, 
                                  Creator, Created, Modified, Subject, Keywords, Description, 
                                  Producer, and PDF Version - or None if extraction fails.
    """
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            info = reader.metadata
            metadata = {
                'Title': info.title if info.title else '',
                'Author': info.author if info.author else '',
                'Creator': info.creator if info.creator else '',
                'Created': info.creation_date if info.creation_date else '',
                'Modified': info.modification_date if info.modification_date else '',
                'Subject': info.subject if info.subject else '',
                'Keywords': info.get('/Keywords', ''),
                'Description': info.get('/Description', ''),
                'Producer': info.producer if info.producer else '',
                'PDF Version': extract_pdf_version(pdf_path)
            }
            return metadata
    except Exception as e:
        print(f"Error processing file {pdf_path}: {e}")
        return None


def write_csv(metadata_list: List[Dict[str, str]], output_file_name: str) -> None:
    """
    Saves the metadata in a CSV file.

    Args:
        metadata_list (List[Dict[str, str]]): List of metadata dictionaries to write.
        output_file (str): Path to or name of the output CSV file.
    """
    if metadata_list:
        keys = metadata_list[0].keys()
        with open(output_file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys, delimiter=';')
        # writer = csv.DictWriter(output_file, fieldnames=keys, delimiter=';')
            writer.writeheader()
            for metadata in metadata_list:
                writer.writerow(metadata)


def process_file(file_path: str, output_file_name: str) -> None:
    """
    Processes a single PDF file, extracts its metadata, and saves it in a CSV file.

    Args:
        file_path (str): Path to the PDF file.
        output_file_name (str): Path to or name of the output CSV file.
    """
    metadata = extract_metadata(file_path)
    if metadata:
        write_csv([metadata], output_file_name)
        print(f"Metadata is saved as {output_file_name}.")


def process_directory(directory_path: str, output_file_name: str) -> None:
    """
    Processes a directory of PDF files, extracts the metadata from each, and saves it all in one CSV file.

    Args:
        directory_path (str): Path to the directory containing PDF files.
        output_file (str): Path to or name of the output CSV file.
    """
    metadata_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                metadata = extract_metadata(file_path)
                if metadata:
                    metadata_list.append(metadata)
    if metadata_list:
        write_csv(metadata_list, output_file_name)
        print(f"Metadata from {len(metadata_list)} files was saved in {output_file_name}.")
    else:
        print("No pdf files found in directory.")


def main() -> None:
    """
    Main function that manages argument parsing and the processing flow for extracting PDF metadata.

    Steps:
    1. **Parse Arguments**:
       - An `argparse.ArgumentParser` object is created to parse the arguments provided by the user for the output file and input file / directory.
       - The `-n` argument (`--name`) accepts a filename or full path where the output CSV file will be saved.
       - The argument group (`-f` or `-d`) allows the user to specify either a single PDF file or a directory containing multiple PDF files.

    2. **Verify and Add File Extension**:
       - The `ensure_csv_extension` function is applied to `args.name` to ensure the output file ends with `.csv` if the user omitted the extension.
       - The result is stored as `output_file_name`, which will later be used to save the CSV file.

    3. **Process Input File or Directory**:
       - If the `-f` argument (file path) is provided and is a valid file, the `process_file` function is called to extract metadata from the single PDF file and save it in CSV format.
       - If the `-d` argument (directory) is provided and is a valid directory, the `process_directory` function is called to extract metadata from all PDF files in the directory and save them in CSV format.

    4. **Error Handling**:
       - If neither a valid file nor a valid directory is found, the script displays an error message and prompts the user to enter a valid path to a PDF file or directory.
    
    Outcome:
       - The metadata from the PDF file(s) is saved as a CSV file at the specified location or current directory.
       - The program provides a confirmation when the CSV file has been successfully created, including the path and, in the case of directories, the number of files processed.

    Example:
       ```shell
       python metapdf.py -n "output.csv" -f "input.pdf"
       ```
       Saves the metadata from the PDF file `input.pdf` into `output.csv` in the current directory.
    """
    parser = argparse.ArgumentParser(description="Extract metadata from pdf files and save them in a csv-file")
 
    parser.add_argument('-n', '--name', type=str, required=True, help="path and/or name of the output file")
    
    # csv-outputfile equivalent
    # parser.add_argument('-n', '--name', type=argparse.FileType('w', encoding='utf-8'), required=True, help="name of the output file")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', type=str, help="path to a single pdf file")
    group.add_argument('-d', '--directory', type=str, help="path to a directory with PDF files")
 
    args = parser.parse_args()

    output_file_name = ensure_csv_extension(args.name) 

    if args.file and os.path.isfile(args.file):
        process_file(args.file, output_file_name)
        # process_file(args.file, args.name)
    elif args.directory and os.path.isdir(args.directory):
        process_directory(args.directory, output_file_name)
        # process_file(args.file, args.name)
    else:
        print("Please enter a valid path to a single pdffile or a directory.")

if __name__ == "__main__":
    main()