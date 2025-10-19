from flask import Flask, request, jsonify
import logging

# Import scraper functions
from walmart_scraper import scrape_walmart
from metro_scraper import scrape_metro
from loblaws_scraper import scrape_loblaws

# Try importing No Frills scraper with fallback
try:
    from nofrills_scraper import scrape_nofrills
except ImportError as e:
    logging.error(f"Failed to import No Frills scraper: {e}")
    scrape_nofrills = lambda item: []

app = Flask(__name__)
application = app  # Expose for Gunicorn

# Setup logging
logging.basicConfig(
    filename='flask_log.txt',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.route('/price')
def get_price():
    item = request.args.get('item')
    city = request.args.get('city')  # still accepted, but not used for filtering

    if not item:
        logging.warning("Missing item in request")
        return jsonify({"error": "Missing item"}), 400

    results = []

    try:
        walmart_results = scrape_walmart(item)
        logging.info(f"Walmart returned {len(walmart_results)} results for '{item}'")
        results.extend(walmart_results)
    except Exception as e:
        logging.error(f"Walmart error: {e}")

    try:
        metro_results = scrape_metro(item)
        logging.info(f"Metro returned {len(metro_results)} results for '{item}'")
        results.extend(metro_results)
    except Exception as e:
        logging.error(f"Metro error: {e}")

    try:
        nofrills_results = scrape_nofrills(item)
        logging.info(f"No Frills returned {len(nofrills_results)} results for '{item}'")
        results.extend(nofrills_results)
    except Exception as e:
        logging.error(f"No Frills error: {e}")

    try:
        loblaws_results = scrape_loblaws(item)
        logging.info(f"Loblaws returned {len(loblaws_results)} results for '{item}'")
        results.extend(loblaws_results)
    except Exception as e:
        logging.error(f"Loblaws error: {e}")

    logging.info(f"Returning {len(results)} total results for item '{item}'")
    return jsonify(results)

@app.route('/healthcheck')
def healthcheck():
    return "OK", 200

if __name__ == '__main__':
    logging.info("Starting Flask server...")
    try:
        app.run(debug=True, port=5000)
    except Exception as e:
        logging.critical(f"Flask failed to start: {e}")
