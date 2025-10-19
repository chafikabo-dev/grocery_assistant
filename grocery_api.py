from flask import Flask, request, jsonify
from walmart_scraper import scrape_walmart
from metro_scraper import scrape_metro
from sobeys_scraper import scrape_sobeys
from nofrills_scraper import scrape_nofrills
from postal_mapper import get_city_from_postal
import json

app = Flask(__name__)

# Load fallback data
with open("product_data.json", "r", encoding="utf-8") as f:
    product_data = json.load(f)

with open("substitutions.json", "r", encoding="utf-8") as f:
    substitutions = json.load(f)

# Define store coverage
store_directory = {
    "Ottawa": ["Walmart", "Metro", "Sobeys", "No Frills"],
    "Toronto": ["Walmart", "Metro", "Sobeys", "No Frills"],
    "Montreal": ["Metro", "Sobeys"]
}

# Helper to safely run scrapers
def safe_scrape(scraper_func, store_name, item):
    try:
        print(f"🔍 Running {store_name} scraper...")
        results = scraper_func(item)
        print(f"✅ {store_name} returned {len(results)} results")
        return results
    except Exception as e:
        print(f"❌ {store_name} scraper failed: {e}")
        return []

@app.route("/price")
def get_price():
    postal_code = request.args.get("postal", "")
    city_param = request.args.get("city", "").strip().title()
    item = request.args.get("item", "").lower()

    city = get_city_from_postal(postal_code) or city_param
    results = []
    scraper_log = {}
    available_stores = store_directory.get(city, [])

    print(f"📍 Query received: item={item}, city={city}, stores={available_stores}")

    # Run scrapers with error handling
    if "Walmart" in available_stores:
        walmart_results = safe_scrape(scrape_walmart, "Walmart", item)
        scraper_log["Walmart"] = len(walmart_results)
        results.extend(walmart_results)

    if "Metro" in available_stores:
        metro_results = safe_scrape(scrape_metro, "Metro", item)
        scraper_log["Metro"] = len(metro_results)
        results.extend(metro_results)

    if "Sobeys" in available_stores:
        sobeys_results = safe_scrape(scrape_sobeys, "Sobeys", item)
        scraper_log["Sobeys"] = len(sobeys_results)
        results.extend(sobeys_results)

    if "No Frills" in available_stores:
        nofrills_results = safe_scrape(scrape_nofrills, "No Frills", item)
        scraper_log["No Frills"] = len(nofrills_results)
        results.extend(nofrills_results)

    # Return live results if found
    if results:
        cheapest = min(results, key=lambda x: x["price"])
        return jsonify({
            "item": item,
            "city": city,
            "postal_code": postal_code,
            "cheapest": cheapest,
            "all_prices": results,
            "source": "live",
            "scraper_log": scraper_log
        })

    # Fallback to static data
    city_data = product_data.get(city)
    if city_data:
        item_prices = city_data.get(item)
        if item_prices:
            cheapest = min(item_prices, key=lambda x: x["price"])
            return jsonify({
                "item": item,
                "city": city,
                "postal_code": postal_code,
                "cheapest": cheapest,
                "all_prices": item_prices,
                "source": "fallback"
            })

    # Suggest alternatives
    suggested = substitutions.get(item)
    if suggested:
        return jsonify({
            "error": "Item not found",
            "suggestions": suggested,
            "city": city,
            "postal_code": postal_code,
            "item": item
        }), 404

    # No match at all
    return jsonify({
        "error": "Item not found",
        "city": city,
        "postal_code": postal_code,
        "item": item
    }), 404

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/healthcheck')
def healthcheck():
    return "OK", 200
