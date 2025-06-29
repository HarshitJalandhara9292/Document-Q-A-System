from PIL import Image
import pytesseract

def ocr_page_image(page) -> str:
    """
    Converts a PyMuPDF page to image and runs OCR on it.
    """
    try:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"[ERROR] OCR failed: {e}"
