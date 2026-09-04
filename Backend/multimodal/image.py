from pathlib import Path
import re
import json
import os
import shutil

from AI.analyzer import analyze_conversation


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

    Returns:
        dict: Standardized multimodal output.
    """

    try:
        try:
            from PIL import Image
            import pytesseract
        except ImportError:
            return {
                "input_type": "image",
                "text": "",
                "language": "unknown",
                "error": "Screenshot OCR is unavailable",
                "detail": "Pillow and pytesseract must be installed on the server.",
            }

        configured_path = os.getenv("TESSERACT_CMD")
        candidate_paths = [
            configured_path,
            shutil.which("tesseract"),
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        tesseract_path = next(
            (Path(path) for path in candidate_paths if path and Path(path).exists()),
            None,
        )
        if tesseract_path is None:
            return {
                "input_type": "image",
                "text": "",
                "language": "unknown",
                "error": "Screenshot OCR is unavailable",
                "detail": "Tesseract OCR is not installed on the server.",
            }

        pytesseract.pytesseract.tesseract_cmd = str(tesseract_path)
        image = Image.open(image_path)

        # Extract text using OCR
        text = pytesseract.image_to_string(image)

        # Clean OCR formatting
        cleaned_text = clean_ocr_text(text)

        return {
            "input_type": "image",
            "text": cleaned_text,
            "language": "unknown"
        }

    except Exception as error:
        return {
            "input_type": "image",
            "text": "",
            "language": "unknown",
            "error": "Screenshot OCR failed",
            "detail": str(error),
        }


def analyze_image(image_path):
    """
    Extract text from an image and send it to the SafeSphere AI analyzer.

    Returns:
        dict: Complete image analysis result.
    """

    # Step 1: OCR
    extracted = extract_text_from_image(image_path)

    # Stop if OCR failed
    if extracted.get("error"):
        return extracted

    # Get extracted text
    text = extracted["text"]

    # Stop if no text was found
    if not text.strip():
        return {
            "input_type": "image",
            "extracted_text": "",
            "analysis": {
                "error": "No text could be extracted from the image"
            }
        }

    # Step 2: Send extracted text to Member 2's AI analyzer
    analysis = analyze_conversation(text)

    # Step 3: Return standardized result
    return {
        "input_type": "image",
        "extracted_text": text,
        "analysis": analysis
    }


if __name__ == "__main__":
    # Find test_chat.png in the project root
    project_folder = Path(__file__).resolve().parents[2]
    image_path = project_folder / "test_chat_hinglish.png"

    if not image_path.exists():
        print(f"Image not found: {image_path}")
    else:
        result = analyze_image(image_path)

        print("\n===== IMAGE PIPELINE OUTPUT =====\n")
        print(json.dumps(result, indent=4, ensure_ascii=False))
