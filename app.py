import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Crypto(db.Model):

    __tablename__ = 'crypto'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))

    def __init__(self, body):

        self.body = body


@app.route('/')
def hello_world():
    return jsonify({'name': 'Liam!'})


@app.route('/posty')
def posty():
    data = Crypto('this is some text')
    db.session.add(data)
    db.session.commit()
    return jsonify({'yes': 'success'})


if __name__ == '__main__':
    app.run()
