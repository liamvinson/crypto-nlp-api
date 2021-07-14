import os
import datetime

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Crypto(db.Model):

    __tablename__ = 'crypto-sentiment-analysis'

    date = db.Column(db.Date(), primary_key=True)
    sentiment = db.Column(db.Float())

    def __init__(self, date, sentiment):

        self.date = date
        self.sentiment = sentiment


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
