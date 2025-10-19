from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_nofrills(item):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    search_url = f"https://www.nofrills.ca/search?search-bar={item.replace(' ', '+')}"
    driver.get(search_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='product-title']"))
        )
    except Exception as e:
        print(f"⚠️ Timeout waiting for product tiles: {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = []
    tiles = soup.select("div[data-testid='price-product-tile']")

    for tile in tiles:
        title_tag = tile.find_next("h3", {"data-testid": "product-title"})
        brand_tag = tile.find_next("p", {"data-testid": "product-brand"})
        price_tag = tile.find("span", {"data-testid": "regular-price"}) or tile.find("span", {"data-testid": "sale-price"})

        name = title_tag.text.strip() if title_tag else ""
        brand = brand_tag.text.strip() if brand_tag else ""
        price_text = price_tag.text.strip().replace("$", "") if price_tag else "0.0"

        try:
            price = float(price_text)
        except ValueError:
            price = 0.0

        if name:
            results.append({
                "store": "No Frills",
                "name": f"{brand} {name}" if brand else name,
                "price": price
            })

    print(f"✅ No Frills returned {len(results)} results")
    return results
