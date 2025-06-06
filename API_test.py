import requests

API_URL = "http://127.0.0.1:8000/extract-text/"
PDF_PATH = "EORY_Telugu_inner.pdf"
LANG = "tel"  # Example: Telugu

with open(PDF_PATH, "rb") as f:
    files = {"file": (PDF_PATH, f, "application/pdf")}
    data = {"lang": LANG}
    response = requests.post(API_URL, files=files, data=data)

if response.ok:
    json_resp = response.json()
    print("Download URL:", json_resp["download_url"])

    # Download the text file
    download_url = "http://localhost:8000" + json_resp["download_url"]
    txt_response = requests.get(download_url)

    if txt_response.ok:
        with open("output.txt", "wb") as out_file:
            out_file.write(txt_response.content)
        print("OCR result saved to output.txt")
    else:
        print("Failed to download the extracted text file.")
else:
    print("API request failed:", response.text)
