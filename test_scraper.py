from walmart_scraper import scrape_walmart
from metro_scraper import scrape_metro
from nofrills_scraper import scrape_nofrills
from loblaws_scraper import scrape_loblaws

def test_scraper(scraper_func, store_name, query):
    print(f"\n🔍 Testing {store_name} scraper with query: '{query}'")
    try:
        results = scraper_func(query)
        if results:
            for r in results:
                print(f"- {r['name']} — ${r['price']} at {r['store']}")
        else:
            print(f"⚠️ No results returned by {store_name} for '{query}'")
    except Exception as e:
        print(f"❌ {store_name} scraper failed: {e}")

if __name__ == "__main__":
    query = "eggs"  # Try "large eggs", "omega-3 eggs", etc.

    test_scraper(scrape_walmart, "Walmart", query)
    test_scraper(scrape_metro, "Metro", query)
    test_scraper(scrape_nofrills, "No Frills", query)
    test_scraper(scrape_loblaws, "Loblaws", query)
