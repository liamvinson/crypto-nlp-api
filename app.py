import os

from flask import Flask, jsonify
from database import db, Crypto


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def hello_world():
    return jsonify({'name': 'Liam!'})


@app.route('/access-data')
def access_data():

    query = db.session.query(Crypto).all()
    data = [{"date": crypto.date.isoformat(), "sentiment": crypto.sentiment} for crypto in query]

    return jsonify({"data": data})


if __name__ == '__main__':
    app.run()
