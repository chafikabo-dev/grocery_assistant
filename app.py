from flask import Flask
app = Flask(__name__)
application = app  # for Gunicorn

@app.route('/healthcheck')
def healthcheck():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
