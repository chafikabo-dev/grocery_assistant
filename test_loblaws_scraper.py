from loblaws_scraper import scrape_loblaws

query = "eggs"
results = scrape_loblaws(query)

print(f"\n🥚 Loblaws Results for '{query}':")
for item in results:
    print(f"- {item['store']}: ${item['price']} ({item['name']})")
