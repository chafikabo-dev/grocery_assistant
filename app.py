from flask import Flask
app = Flask(__name__)
application = app  # 👈 Critical for Gunicorn

@app.route('/healthcheck')
def healthcheck():
    return '', 200

app.run(host="0.0.0.0", port=8080)
@app.route("/")
def home():
    return "Home is live!"
