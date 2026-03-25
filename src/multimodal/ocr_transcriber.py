import easyocr
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image_path)
    text = " ".join([r[1] for r in results])
    return text