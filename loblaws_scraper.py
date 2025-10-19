from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_loblaws(item):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    search_url = f"https://www.loblaws.ca/search?search-bar={item.replace(' ', '+')}"
    driver.get(search_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3[data-testid='product-title']"))
        )
    except Exception as e:
        print(f"⚠️ Timeout or error: {e}")
        driver.quit()
        return []

    # Scroll to bottom to trigger lazy loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Save raw HTML for inspection
    with open("loblaws_debug.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = []
    product_titles = soup.select("h3[data-testid='product-title']")

    for title in product_titles:
        parent = title.find_parent("div", {"data-testid": "price-product-tile"})
        if not parent or "Sponsored" in parent.text:
            continue

        brand = parent.select_one("p[data-testid='product-brand']")
        price_tag = parent.select_one("span[data-testid='regular-price']") or parent.select_one("span[data-testid='sale-price']")

        name = title.text.strip()
        brand_name = brand.text.strip() if brand else ""
        price_text = price_tag.text.strip().replace("$", "") if price_tag else "0.0"

        try:
            price = float(price_text)
        except ValueError:
            price = 0.0

        results.append({
            "store": "Loblaws",
            "name": f"{brand_name} {name}" if brand_name else name,
            "price": price
        })

    print(f"✅ Loblaws returned {len(results)} results for '{item}'")
    return results
