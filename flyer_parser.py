from PIL import Image
import pytesseract
import os

def parse_flyer_image(image_path, store_name="Flyer Store"):
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return []

    flyer_text = pytesseract.image_to_string(Image.open(image_path))
    lines = flyer_text.split("\n")
    results = []

    for line in lines:
        if "$" in line:
            parts = line.split("$")
            name = parts[0].strip()
            try:
                price = float(parts[1].strip().replace(",", "."))
            except ValueError:
                price = 0.0
            results.append({
                "store": store_name,
                "name": name,
                "price": price
            })

    print(f"✅ Parsed {len(results)} items from {store_name} flyer")
    return results
