import os
import fitz  
from loaders.ocr_utils import ocr_page_image

def extract_text_from_pdf(file_path: str, force_ocr: bool = False) -> str:
    """
    Extracts text from a PDF. Uses OCR for scanned PDFs if force_ocr is True.
    """
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            if force_ocr:
                text += ocr_page_image(page)
            else:
                page_text = page.get_text()
                if page_text.strip():
                    text += page_text
                else:
                    # Fallback to OCR for blank or image-only pages
                    text += ocr_page_image(page)
    except Exception as e:
        return f"[ERROR] Failed to extract PDF text: {e}"
    return text

def extract_text_from_txt(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"[ERROR] Failed to read TXT file: {e}"

def load_file(file_path: str, force_ocr: bool = False) -> str:
    """
    Dispatches the right extractor based on file type.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path, force_ocr=force_ocr)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        return f"[ERROR] Unsupported file type: {ext}"

