from flask import Flask

app = Flask(__name__)
application = app

@app.route('/healthcheck')
def healthcheck():
    return "OK", 200
