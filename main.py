from flask import Flask
from waitress import serve

from loacator.services import get_location

app = Flask(__name__)

@app.route('/')
def get_location_api():
    return get_location('http://api.open-notify.org/iss-now.json')

if __name__ == '__main__':
    serve(app)
