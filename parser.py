# parser.py
from pdfminer.high_level import extract_text
from docx import Document
import os

def read_pdf(path):
    return extract_text(path)

def read_docx(path):
    doc = Document(path)
    return '\n'.join([p.text for p in doc.paragraphs if p.text.strip()])

def extract_raw_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext in [".docx", ".doc"]:
        return read_docx(path)
    else:
        raise ValueError("Unsupported file format!")

if __name__ == "__main__":
    # Test
    resume_path = "sample_resume.pdf"
    text = extract_raw_text(resume_path)
    print(text)
# parser.py