import logging
import time
from flask import Flask

# Delay to give Gunicorn time to boot before healthcheck
time.sleep(2)

logging.basicConfig(level=logging.INFO)
logging.info("✅ Flask app loaded successfully")

app = Flask(__name__)
application = app  # Required for Gunicorn

@app.route("/")
def home():
    return "✅ Minimal Flask app is live!"

@app.route("/healthcheck")
def healthcheck():
    return "", 200
