# Copyright (C) 2023-2025 Cognizant Digital Business, Evolutionary AI.
# All Rights Reserved.
# Issued under the Academic Public License.

import os
from io import BytesIO
import fitz  # PyMuPDF

from typing import Dict, Any, List, Union

from google import genai  
from google.genai import types
from neuro_san.interfaces.coded_tool import CodedTool


class VisualContentAnalyzer(CodedTool):
    """
    Visual Content Analyzer for detecting inappropriate or sensitive visual content
    within PDF documents using Gemini 2.5 multimodal capabilities.
    """

    def __init__(self):
        """
        Initialize the Gemini client for multimodal analysis.
        Requires GOOGLE_API_KEY to be set in environment variables.
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise EnvironmentError("Missing GOOGLE_API_KEY environment variable.")

        # Configure Gemini client
        self.client = genai.Client(api_key=api_key)



    def _convert_pdf_pages_to_images(self, pdf_path: str) -> List[bytes]:
        """
        Converts each page of the PDF into a PNG image (as bytes).
        """
        images_bytes = []
        doc = fitz.open(pdf_path)

        for page in doc:
            pix = page.get_pixmap(dpi=200)
            buffer = BytesIO()
            buffer.write(pix.tobytes("png"))
            images_bytes.append(buffer.getvalue())

        return images_bytes



    # def _extract_images_from_pdf(self, pdf_path: str) -> List[bytes]:
    #     """
    #     Extracts all images from a PDF and returns them as raw bytes.

    #     :param pdf_path: Path to the PDF file.
    #     :return: List of image bytes.
    #     """
    #     images_bytes = []

    #     with fitz.open(pdf_path) as pdf:
    #         for page_index in range(len(pdf)):
    #             page = pdf[page_index]
    #             images = page.get_images(full=True)

    #             for img_index, img in enumerate(images, start=1):
    #                 xref = img[0]
    #                 base_img = pdf.extract_image(xref)
    #                 image_bytes = base_img["image"]
    #                 images_bytes.append(image_bytes)

    #     return images_bytes

    def _analyze_image_with_gemini(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Uses Gemini multimodal API to classify inappropriate or sensitive content.
        """
        # Gemini request prompt
        prompt = """
        You are a compliance assistant.
        Analyze this image and classify if it contains any of the following:
        - Violence
        - Sexual or explicit content
        - Medical explicitness (like brain scanner)
        - Nudity or unsafe material
        Otherwise, classify it as SAFE.
        Return the response in JSON format with fields:
        {
            "safe": true/false,
            "categories": [list of detected categories],
            "recommendation": "short remediation guidance"
        }
        """

        # Convertimos la imagen en un Part
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png"  # ajusta según el tipo real de la imagen
        )

        # Llamamos al modelo
        result = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image_part]
        )

        return result.text

    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        """
        Main entry point for VisualContentAnalyzer.

        :param args: Expected keys:
                     - "pdf_path" (str): Path to the PDF file.
        :param sly_data: Metadata passed by orchestrator (not used here).
        :return: JSON with analysis results or an error string.
        """
        try:
            pdf_path: str = args.get("pdf_path", None)
            if pdf_path is None or not os.path.exists(pdf_path):
                return "Error: A valid PDF file path must be provided."

            # Extract images from PDF
            page_images = self._convert_pdf_pages_to_images(pdf_path)

            if not page_images:
                return {
                    "status": "success",
                    "message": "No images found in the PDF.",
                    "analysis": []
                }

            # Analyze each image
            analysis_results = []
            for idx, img_bytes in enumerate(page_images, start=1):
                try:
                    result = self._analyze_image_with_gemini(img_bytes)
                    analysis_results.append({
                        "page_number": idx,
                        "result": result
                    })
                except Exception as e:
                    analysis_results.append({
                        "page_number": idx,
                        "error": str(e)
                    })

            return {
                "status": "success",
                "message": "Visual content analysis completed successfully.",
                "analysis": analysis_results
            }

        except Exception as e:
            return f"Error: {str(e)}"
 