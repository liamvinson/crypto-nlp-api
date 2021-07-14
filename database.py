from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Crypto(db.Model):

    __tablename__ = 'crypto-sentiment-analysis'

    date = db.Column(db.Date(), primary_key=True)
    sentiment = db.Column(db.Float())

    def __init__(self, date, sentiment):

        self.date = date
        self.sentiment = sentiment
