import logging
logging.basicConfig(level=logging.INFO)
logging.info("✅ Flask app loaded successfully")



from flask import Flask

app = Flask(__name__)
application = app  # Required for Gunicorn

@app.route("/")
def home():
    return "✅ Minimal Flask app is live!"

@app.route("/healthcheck")
def healthcheck():
    return "OK", 200
