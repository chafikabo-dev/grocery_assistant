import logging
from flask import Flask

# Log startup to confirm container is alive
logging.basicConfig(level=logging.INFO)
logging.info("✅ Flask app loaded successfully")

app = Flask(__name__)
application = app  # Required for Gunicorn

@app.route("/")
def home():
    return "✅ Minimal Flask app is live!"

@app.route("/healthcheck")
def healthcheck():
    return "OK", 200
