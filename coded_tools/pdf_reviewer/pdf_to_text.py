# Copyright (C) 2023-2025 Cognizant Digital Business, Evolutionary AI.
# All Rights Reserved.
# Issued under the Academic Public License.
#
# You can be released from the terms, and requirements of the Academic Public
# License by purchasing a commercial license.
# Purchase of a commercial license is mandatory for any use of the
# neuro-san-studio SDK Software in commercial settings.
#
from typing import Any
from typing import Dict
from typing import Union
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os

from neuro_san.interfaces.coded_tool import CodedTool


class PDFToTextExtractor(CodedTool):
    """
    CodedTool implementation for extracting text from PDF files.
    Supports both text-based PDFs and scanned PDFs (via OCR).
    """

    def __init__(self):
        """
        Constructs the PDF to Text Extractor.
        Configure the Tesseract path if required.
        """
        # Uncomment and set the correct Tesseract path if needed (for Windows users)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pass

    def _extract_text(self, pdf_path: str) -> str:
        """
        Extracts text from a PDF file using PyMuPDF and Tesseract OCR.

        :param pdf_path: Path to the input PDF file.
        :return: Extracted text as a single string.
        """
        extracted_text = ""

        # Open the PDF file
        with fitz.open(pdf_path) as pdf:
            # print(f"Processing '{pdf_path}' ({pdf.page_count} pages)...")

            for num, page in enumerate(pdf, start=1):
                # print(f"Extracting text from page {num}...")

                # Attempt direct text extraction
                text = page.get_text()

                if text.strip():
                    extracted_text += f"\n--- PAGE {num} ---\n" + text
                else:
                    # If the page contains only images, apply OCR
                    # print(f"  → Page {num} appears to be an image, applying OCR...")
                    pix = page.get_pixmap()
                    img_bytes = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_bytes))

                    # OCR with pytesseract (English by default)
                    ocr_text = pytesseract.image_to_string(img, lang="eng")
                    extracted_text += f"\n--- PAGE {num} (OCR) ---\n" + ocr_text

        return extracted_text

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        :param args: Argument dictionary whose keys are the parameters
                to the coded tool and whose values are passed by the calling agent.
                Expected keys:
                    "pdf_path" (str): Absolute path to the PDF file.
                    "output_txt" (optional, str): Path where the extracted text will be saved.

        :param sly_data: Dictionary whose keys are defined by the agent hierarchy.
                It is generally treated as read-only.

        :return:
            On success:
                {
                    "text": "<extracted_text>",
                    "message": "Text successfully extracted"
                }
            On failure:
                "Error: <error_message>"
        """
        try:
            pdf_path: str = args.get("pdf_path", None)
            output_path: str = args.get("output_txt", "extracted_text.txt")

            if pdf_path is None or not os.path.exists(pdf_path):
                return "Error: A valid PDF file path must be provided."

            # print(">>>>>>>>>>>>>>>>>>> PDFToTextExtractor >>>>>>>>>>>>>>>")
            # print(f"PDF File: {pdf_path}")

            # Extract text from the PDF
            extracted_text = self._extract_text(pdf_path)

            # Save the extracted text to a file
            # with open(output_path, "w", encoding="utf-8") as f:
            #     f.write(extracted_text)

            # print(f"Text successfully extracted and saved to: {output_path}")
            # print(">>>>>>>>>>>>>>>>>>> DONE !!! >>>>>>>>>>>>>>>")

            return {
                "text": extracted_text,
                "message": "Text successfully extracted" 
            }

        except Exception as e:
            return f"Error: {str(e)}"
 