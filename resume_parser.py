import fitz  # PyMuPDF

def extract_text(pdf):
    text = ""

    doc = fitz.open(stream=pdf.read(), filetype="pdf")

    for page in doc:
        text += page.get_text()

    return text

