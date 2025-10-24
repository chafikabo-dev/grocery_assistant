import logging
from flask import Flask

# Setup logging to confirm app load
logging.basicConfig(level=logging.INFO)
logging.info("✅ Flask app loaded successfully")

app = Flask(__name__)
application = app  # 👈 Critical for Gunicorn

@app.route('/healthcheck')
def healthcheck():
    return '', 200

@app.route('/')
def home():
    return "Home is live!"
