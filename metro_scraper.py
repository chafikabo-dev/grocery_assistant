import requests
from bs4 import BeautifulSoup

def scrape_metro(item):
    results = []
    search_url = f"https://www.metro.ca/en/search?filter={item.replace(' ', '+')}"

    try:
        response = requests.get(search_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select(".default-product-tile")

        for product in products:
            name = product.get("data-product-name", "").strip()
            brand_tag = product.select_one(".head__brand")
            title_tag = product.select_one(".head__title")
            size_tag = product.select_one(".head__unit-details")
            price_tag = product.select_one(".price-update")

            brand = brand_tag.get_text(strip=True) if brand_tag else ""
            title = title_tag.get_text(strip=True) if title_tag else ""
            size = size_tag.get_text(strip=True) if size_tag else ""
            price_text = price_tag.get_text(strip=True).replace("$", "").replace(",", ".") if price_tag else ""

            try:
                price = float(price_text)
                full_name = f"{brand} {title} {size}".strip()
                results.append({ "store": "Metro", "name": full_name, "price": price })
            except ValueError:
                continue

    except Exception as e:
        print(f"⚠️ Metro scraping error: {e}")

    print(f"✅ Metro returned {len(results)} results")
    return results
