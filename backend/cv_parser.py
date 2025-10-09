import pdfplumber
import logging

logger = logging.getLogger(__name__)

 # exceptions +
def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file"""
    try:
        with pdfplumber.open(file_bytes) as pdf:
            if not pdf.pages:
                raise ValueError("PDF has no pages")

            text = ""
            for page in pdf.pages:
                text_page = page.extract_text()
                if text_page:
                    text += text_page + "\n\n"

            if not text or len(text.strip()) < 20:
                raise ValueError("PDF contains insufficient text")

            logger.debug(f"Successfully extracted {len(text.strip())} characters")
            return text

    except ValueError:
        raise

    except Exception as e:
        error_type = type(e).__name__
        logger.debug(f"PDF parsing error ({error_type}): {e}")
        raise ValueError(f"PDF is corrupted or invalid: {str(e)}")