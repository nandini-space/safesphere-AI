from pathlib import Path
import re

from PIL import Image
import pytesseract


# Tell pytesseract where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def clean_ocr_text(text):
    """
    Clean basic OCR formatting without changing the actual meaning.
    """

    # Normalize Windows/Linux line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove spaces at the beginning/end of lines
    lines = [line.strip() for line in text.split("\n")]

    # Remove completely empty lines
    lines = [line for line in lines if line]

    # Reduce repeated spaces
    lines = [re.sub(r"\s+", " ", line) for line in lines]

    # Join the cleaned lines
    cleaned_text = "\n".join(lines)

    return cleaned_text.strip()


def extract_text_from_image(image_path):
    """
    Extract text from an image using Tesseract OCR.
    """

    image = Image.open(image_path)

    # Extract text
    text = pytesseract.image_to_string(image)

    # Clean basic OCR formatting
    cleaned_text = clean_ocr_text(text)

    return cleaned_text


if __name__ == "__main__":

    # Find test_chat.png in the same folder as this Python file
    project_folder = Path(__file__).resolve().parents[2]
    image_path = project_folder / "test_chat.png"

    extracted_text = extract_text_from_image(image_path)

    print("\n===== EXTRACTED TEXT =====\n")
    print(extracted_text)