# METAPDF

This program extracts metadata from PDF files and saves it in a CSV file at a specified location. The user can specify either a single PDF file or a directory containing multiple PDFs.    

The program was created as part of my training at the Developer Academy and is used exclusively for teaching purposes.  

It was coded on **Windows 10** using **VSCode** as code editor.

## Table of Contents
1. <a href="#technologies">Technologies</a>  
2. <a href="#features">Features</a>  
3. <a href="#getting-started">Getting Started</a>  
4. <a href="#usage">Usage</a>  
5. <a href="#additional-notes">Additional Notes</a>  

## Technologies
* **Python** 3.12.2
    * **PyPDF2** 3.0.1 (module to install, <a href="https://pypi.org/project/PyPDF2/">More Information</a>)
    * **argparse, csv** (modules from standard library) 

## Features
The following table shows which functions **Metapdf** supports:  

| Flag | Description | Required |
| ---- | ----------- | -------- |
| -h <br> --help | Get a list of the available options | no
| -n <br> --name | Path to or name of the output file | yes |
| -f <br> --file | Path to a single PDF file | yes, if no -d |
| -d <br> --directory | Path to a directory with PDF files | yes, if no -f |

Flow of the Function

- First it is ensured that the output file ends with `.csv` if the user omitted the extension.
- Then the following metadata from the PDF file(s) are extracted:
    - Title
    - Author 
    - Creator
    - Created At
    - Modified At
    - Subject
    - Keywords
    - Description 
    - Producer
    - PDF Version
- In the last step the metadata is saved in a CSV file with the given name and location. 

## Getting Started
0) <a href="https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo">Fork</a> the project to your namespace, if you want to make changes or open a <a href="https://docs.github.com/de/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests">Pull Request</a>.
1) <a href="https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository">Clone</a> the project to your platform if you just want to use the program.
    - <ins>Example</ins>: Clone the repo e.g. using an SSH-Key:  
    `git clone git@github.com:SarahZimmermann-Schmutzler/metapdf.git`
2) Install the dependencies. In this case it's just **PyPDF2**. You can install it across platforms with **Pip**:  
    `pip install PyPDF2`  

## Usage
- Make sure you are in the folder where you cloned **Metapdf** into.  

- Help! What options does the program support!?  
    `python metapdf.py -h`  
    or  
    `python metapdf.py --help`  

- To extract metadata from a **single PDF file**:  
    `python metapdf.py -f [path/to/pdf/file] -n [pathOrNameOfOutputFile]`  
    - <ins>Example</ins>: Extract the metadata from a learning script and save it in a file with the name metadata_script.csv:  
    `python metapdf.py -f "Users/MyName/DeveloperAkademie/learning_script.pdf" -n metadata_script`  
    - The file *metadata_script.csv* that includes all metadata from the PDF file *learning_script* is saved in the current directory. It is irrelevant whether the name of the output file has a .csv extension or not. 

- To extract metadata from **PDF files saved in a directory**:  
    `python metapdf.py -d [path/to/directory/with/pdf/file(s)] -n [pathOrNameOfOutputFile]`  
    - <ins>Example</ins>: Extract the metadata from all learning scripts that are saved in a directory and save it in a file with the name metadata_learning_scripts.csv:  
    `python metapdf.py -d "Users/MyName/DeveloperAkademie/learning_scripts" -n "Users/MyName/DeveloperAkademie/metadata_learning_scripts.csv"`
    - The file *metadata_learning_scripts.csv* that includes all metadata from PDF files of the directory *learning_scripts* is saved in the directory *Users/MyName/DeveloperAkademie*. 
        
- What you see, if the extraction and saving was succesful:  
    ```
    Metadata is saved as [nameOfOutputFile].csv.
    ```

## Additional Notes
**PyPDF2** is a third-party Python library used for working with PDF files. It allows users to perform various operations on PDF files, including reading, writing, merging, and extracting text and metadata. It's a popular choice for handling PDF files in Python because it provides a relatively straightforward interface for interacting with these file types. 
  
The **argparse** module is used to parse (read) command line arguments in Python programs. It allows to define arguments and options that can be passed to the program when starting it from the command line. These are then processed and are available in the program as variables.  
  
The **csv** module allows you to read and write comma-separated values ​​(CSV) files. CSV files are text files that store data in tabular form, with values ​​usually separated by commas (or other separators such as semicolons). They are often used to exchange data between different applications such as spreadsheets, databases and programs.  
  
**ChatGPT** was involved in the creation of the program (Debugging, Prompt Engineering etc.).  
  
I use **Google Translate** for translations from German into English.
