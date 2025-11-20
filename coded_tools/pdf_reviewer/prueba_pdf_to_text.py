import os
import numpy as np
from typing import Any, Dict, Union
from neuro_san.interfaces.coded_tool import CodedTool
import fitz  # PyMuPDF
import easyocr
from PIL import Image
import io


class PDFToTextTool(CodedTool):
    def __init__(self):
        self.name = "PDFToTextTool"
        self.reader = easyocr.Reader(['en', 'es'], gpu=False)

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        pdf_path = args.get("pdf_path")

        if not pdf_path or not os.path.exists(pdf_path):
            return "Error: PDF file path is missing or does not exist."

        try:
            doc = fitz.open(pdf_path)
            extracted_text = ""

            for i, page in enumerate(doc):
                pix = page.get_pixmap()
                img_bytes = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                image_np = np.array(image)  # ← Conversión segura
                results = self.reader.readtext(image_np, detail=0)
                page_text = "\n".join(results)
                extracted_text += f"\n--- Page {i + 1} ---\n{page_text.strip()}\n"

            doc.close()

            return {
                "text": extracted_text.strip(),
                "message": "PDF successfully converted to text using EasyOCR and PyMuPDF."
            }

        except Exception as e:
            return f"Error: Failed to process PDF. Details: {str(e)}"
