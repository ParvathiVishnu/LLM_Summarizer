import os
import tempfile
import docx2txt
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def extract_text_from_txt(file_path):
    """Extract text from plain .txt file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try fallback to default encoding
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading TXT file with fallback {file_path}: {e}")
            return ""
    except Exception as e:
        print(f"❌ Error reading TXT file {file_path}: {e}")
        return ""


def extract_text_from_docx(file_path):
    """Extract text from .docx file"""
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"❌ Error reading DOCX file {file_path}: {e}")
        return ""


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF using PyPDF2.
    If no text is extracted, fallback to OCR using pdf2image + pytesseract.
    """
    try:
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        if text.strip():
            return text
    except Exception as e:
        print(f"❌ Error reading PDF with PyPDF2: {e}")

    # OCR fallback
    try:
        print("🔁 Falling back to OCR for PDF...")
        text = ""
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_path(file_path, output_folder=path)
            for img in images:
                text += pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"❌ OCR fallback failed for PDF {file_path}: {e}")
        return ""


def extract_text_from_file(file_path):
    """Extract text based on file extension"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    else:
        print(f"⚠️ Unsupported file format: {file_path}")
        return ""

