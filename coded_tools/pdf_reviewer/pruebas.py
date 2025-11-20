import os
import io
from typing import Any, Dict, Union
from neuro_san.interfaces.coded_tool import CodedTool
import fitz  # PyMuPDF
from PIL import Image
# import google.generativeai as genai
from google import genai  
from google.genai import types
#from google.generativeai.types import Content, Part

from io import BytesIO

GOOGLE_API_KEY= "AIzaSyDdHjO2EabK6XwIUif1g1N-7KSLif69c5g" # "AIzaSyDXT84sOWY4QJkKBD5tK8Ra1zjBdUNJ-fw"
GOOGLE_MODEL_NAME="gemini-2.5-flash"

def convert_pdf_to_images(pdf_path, output_folder="output_pages"):
    doc = fitz.open(pdf_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        pix = page.get_pixmap(dpi=200)  # Puedes ajustar el DPI para mejor calidad
        output_path = f"{output_folder}/page_{page_number + 1}.png"
        pix.save(output_path)

    print(f"PDF convertido a imágenes en: {output_folder}")

def _convert_pdf_pages_to_images2(pdf_path: str) -> list[bytes]:
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

def _analyze_image_with_gemini(image_bytes: bytes) -> Dict[str, Any]:
    """
    Uses Gemini multimodal API to classify inappropriate or sensitive content.
    """
    # Gemini request prompt
    prompt = """
    You are a compliance assistant.
    Analyze this image and classify if it contains any of the following:
    - Violence
    - Sexual or explicit content
    - Medical explicitness
    - Nudity or unsafe material
    Otherwise, classify it as SAFE.
    Return the response in JSON format with fields:
    {
        "safe": true/false,
        "categories": [list of detected categories],
        "recommendation": "short remediation guidance"
    }
    """
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Convertimos la imagen en un Part
    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/png"  # ajusta según el tipo real de la imagen
    )

    # Llamamos al modelo
    result = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image_part]
    )

    return result.text

# class PDFToTextTool(CodedTool):
#     def __init__(self):
#         self.name = "PDFToTextTool"
#         genai.configure(api_key=GOOGLE_API_KEY)
#         self.model = genai.GenerativeModel("gemini-2.5-flash")


#     def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
#         pdf_path = args.get("pdf_path")

#         if not pdf_path or not os.path.exists(pdf_path):
#             return "Error: PDF file path is missing or does not exist."

#         try:
#             doc = fitz.open(pdf_path)
#             extracted_text = ""

#             for i, page in enumerate(doc):
#                 pix = page.get_pixmap()
#                 img_bytes = pix.tobytes("png")
#                 image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

#                 # Construir contenido multimodal
#                 contents = [
#                     Content(parts=[
#                         Part(text="Extract all readable text from this image."),
#                         Part(image=image)
#                     ])
#                 ]

#                 response = self.model.generate_content(contents)
#                 page_text = response.text.strip()
#                 extracted_text += f"\n--- Page {i + 1} ---\n{page_text}\n"

#             doc.close()

#             return {
#                 "text": extracted_text.strip(),
#                 "message": "PDF successfully converted to text using Gemini 2.5 Flash OCR."
#             }

#         except Exception as e:
#             return f"Error: Failed to process PDF. Details: {str(e)}"



if __name__ == "__main__":
    # Ruta al PDF que quieres probar
    test_pdf_path = "C:\\Users\\2373231\\Downloads\\prueba.pdf"  # ← Cambia esta ruta si es necesario
    p = _convert_pdf_pages_to_images2(test_pdf_path)
    analysis_results = []
    for idx, img_bytes in enumerate(p, start=1):
                
        result = _analyze_image_with_gemini(img_bytes)
        analysis_results.append({
            "image_number": idx,
            "result": result
        })

    print(analysis_results)

    # # Crear instancia de la tool
    # tool = PDFToTextTool()

    # # Ejecutar la tool con argumentos simulados
    # result = tool.invoke({"pdf_path": test_pdf_path}, sly_data={})

    # # Mostrar resultados
    # if isinstance(result, dict):
    #     print(result["message"])
    #     print("\nTexto extraído:\n")
    #     print(result["text"])
    # else:
    #     print(result)
