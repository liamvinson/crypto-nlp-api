from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#
#   Database Models
#


class Crypto(db.Model):

    __tablename__ = 'crypto-sentiment-analysis'

    date = db.Column(db.Date(), primary_key=True)
    sentiment = db.Column(db.Float())

    def __init__(self, date, sentiment):

        self.date = date
        self.sentiment = sentiment


#
#   Database Access Functions
#


def get_data(database):

    query = database.session.query(Crypto).all()
    data = [{"date": crypto.date.isoformat(), "sentiment": crypto.sentiment} for crypto in query]

    return data


def get_dates(database):

    query = database.session.query(Crypto).all()
    dates = [crypto.date for crypto in query]

    return dates


def insert_data(database, data):

    for date, sentiment in data:

        if database.session.query(Crypto).filter(Crypto.date == date).count() == 0:
            data = Crypto(date, sentiment)
            db.session.add(data)
            db.session.commit()
