from sobeys_scraper import scrape_sobeys

results = scrape_sobeys("eggs")
print("\n🥚 Sobeys Results for 'eggs':")
for item in results:
    print(f"- {item['store']}: ${item['price']} ({item['name']})")
