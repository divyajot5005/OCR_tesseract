OCR Narris
This project provides a simple OCR (Optical Character Recognition) API built using FastAPI that extracts text from PDF files using Tesseract OCR, and a corresponding test script to call the API and download the results.

Prerequisites
Before running the scripts, ensure the following are installed on your Linux system:

Python 3.8+
pip
Tesseract OCR
Poppler-utils (for pdf2image backend)
Required Python packages
Install Tesseract and Poppler
sudo apt update
sudo apt install tesseract-ocr poppler-utils
Note: Language packs can be installed for specific languages (e.g., tesseract-ocr-telugu for Telugu support).

Install Python Dependencies
pip install fastapi uvicorn pytesseract pdf2image pillow requests
Running the OCR API
Start the FastAPI server:
uvicorn OCR_API:app --reload
The API will be available at http://127.0.0.1:8000.
🧪 Testing the API
Edit the API_test.py file to specify:

The path to your PDF file (PDF_PATH)
The language code for OCR (e.g., "eng", "tel", "eng+tel")
Run the test script:

python API_test.py
If successful:

You’ll get a printed download URL.
The extracted text will be saved to output.txt.
Output Files
All OCR results are saved in the API_output/ directory, with filenames based on the original PDF name and timestamp.

Notes
Only PDF files are supported.
Ensure tesseract is available at /usr/bin/tesseract or modify TESSERACT_PATH in OCR_API.py.
The FastAPI server must be running before executing API_test.py.
