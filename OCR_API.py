from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import tempfile
import os
from datetime import datetime
app = FastAPI()
# --- Configuration ---
TESSERACT_PATH = "/usr/bin/tesseract"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
OUTPUT_DIR = "API_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
@app.post("/extract-text/")
async def extract_text(
    file: UploadFile = File(...),
    lang: str = Form(..., description="Tesseract language(s) code, e.g., 'eng', 'tel', 'hin', 'eng+tel'")
):
    if not file.filename.lower().endswith('.pdf'):
        return JSONResponse(status_code=400, content={"error": "Only PDF files are supported."})
    contents = await file.read()
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            images = convert_from_bytes(contents, dpi=300)

            full_text = ""
            for i, image in enumerate(images):
                print(f"OCR Page {i+1} using lang='{lang}'")
                text = pytesseract.image_to_string(image, lang=lang)
                full_text += f"\n--- Page {i + 1} ---\n{text}\n"
            # Save output to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(file.filename)[0]
            txt_filename = f"{base_name}_{timestamp}.txt"
            txt_path = os.path.join(OUTPUT_DIR, txt_filename)

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            return {"download_url": f"/download/{txt_filename}"}

    except pytesseract.TesseractError as te:
        return JSONResponse(status_code=500, content={"error": "Tesseract OCR failed", "details": str(te)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "details": str(e)})

@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='text/plain')
    return JSONResponse(status_code=404, content={"error": "File not found."})