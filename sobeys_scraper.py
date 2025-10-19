from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_sobeys(item):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    search_url = f"https://www.sobeys.com/en/search/?q={item.replace(' ', '+')}"
    driver.get(search_url)

    # Wait for product tiles to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.tab"))
        )
    except Exception as e:
        print(f"⚠️ Timeout waiting for product tiles: {e}")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = []
    products = soup.select("a.tab")

    for product in products:
        label = product.get("aria-label", "")
        name = label.replace("Click here to go to ", "").replace(" product detail page", "").strip()
        if name:
            results.append({
                "store": "Sobeys",
                "name": name,
                "price": 0.0  # Placeholder until we scrape detail pages
            })

    print(f"✅ Sobeys returned {len(results)} results")
    return results
