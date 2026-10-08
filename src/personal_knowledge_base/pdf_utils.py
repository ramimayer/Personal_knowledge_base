
from pathlib import Path
import os

from pdf2image import convert_from_path 
import pytesseract
from langchain_community.document_loaders import PyPDFLoader

# Add this line and verify the path matches your installation folder
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#----------------------------------------------------------------------------------------
def pdf_to_txt(input_file_path: str, filename: str, output_folder: str):
    pdf_loader = PyPDFLoader(input_file_path)
    print("pdf_to_txt(): input_file_path = " + input_file_path + ", output_folder = " + output_folder)
    pages = pdf_loader.load()

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    output_file_path = output_folder + "/" + filename + ".txt"

    # Check if the output file already exists
    if os.path.exists(output_file_path):
        return

    # 2 different cases:  if the PDF is made of scans - use OCR first, else simply write the text to a  file
    if (needs_ocr(input_file_path)):
        print("pdf_to_txt(): needs_ocr() = True, calling ipdf2txt()")
        with open(output_file_path, "w", encoding="utf-8") as f:
            text = ipdf2txt(input_file_path)
            f.write(text)
    else:
        print("pdf_to_txt(): needs_ocr() = False, calling pdf_loader.load()")
        with open(output_file_path, "w", encoding="utf-8") as f:
            for page in pages:
                f.write(page.page_content)
                f.write("\n\n" + "="*40 + "\n\n")  # Add a separator between documents

#----------------------------------------------------------------------------------------
def needs_ocr(file_path: str) -> bool:
    # Check if the file is a PDF
    if not file_path.lower().endswith('.pdf'):
        return False

    # Load the PDF and check if it contains any text
    pdf_loader = PyPDFLoader(file_path)
    pages = pdf_loader.load()
    for page in pages:
        if page.page_content.strip():  # If there's any non-whitespace content
            return False  # No OCR needed

    return True  # OCR needed since no text was found

#----------------------------------------------------------------------------------------
def ipdf2txt(pdf_path):
    # Step 1: Convert PDF pages to a list of images
    images = convert_from_path(pdf_path)

    # Step 2: Iterate through images and extract text using Tesseract
    extracted_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        extracted_text += f"--- Page {i + 1} ---\n" + text + "\n\n"

    return extracted_text
