from nofrills_scraper import scrape_nofrills

results = scrape_nofrills("eggs")
print("\n🥚 No Frills Results for 'eggs':")
for item in results:
    print(f"- {item['store']}: ${item['price']} ({item['name']})")
