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


@app.route('/posty')
def posty():
    data = Crypto(datetime.date.today(), 0.364)
    db.session.add(data)
    db.session.commit()
    return jsonify({'yes': 'success'})


if __name__ == '__main__':
    app.run()
