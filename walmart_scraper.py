import requests
from bs4 import BeautifulSoup
import json

def scrape_walmart(item):
    print(f"🔍 Starting scrape for: {item}")
    search_url = f"https://www.walmart.ca/search?q={item}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")

    results = []
    if script_tag:
        try:
            data = json.loads(script_tag.string)
            items = data["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]

            for product in items[:3]:
                name = product.get("name")
                price = product.get("price")

                if name and isinstance(price, (int, float)):
                    results.append({
                        "name": name,
                        "price": float(price),
                        "store": "Walmart"
                    })
        except Exception as e:
            print("❌ Failed to parse JSON:", e)
    else:
        print("❌ JSON script tag not found")

    return results

# 👇 Run this to test directly
