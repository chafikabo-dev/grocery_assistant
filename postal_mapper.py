postal_to_city = {
    "K1A": "Ottawa",
    "M5A": "Toronto",
    "H2X": "Montreal"
}

def get_city_from_postal(postal_code):
    prefix = postal_code.strip().upper()[:3]
    return postal_to_city.get(prefix)
