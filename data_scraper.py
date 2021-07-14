# Import required modules.
import datetime

import spacy
import requests
import pandas as pd
from spacytextblob.spacytextblob import SpacyTextBlob

# Setup spacy nlp pipeline
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob");


def filter_existing_submissions(df, dates):
    date_series = df.date.dt.date
    df = df[~date_series.isin(dates)]

    return df


def get_submissions(dates=None):
    # Request all comments from submission.
    url = 'https://api.pushshift.io/reddit/search/submission/'
    params = {
        'subreddit': 'CryptoCurrency',
        'size': 300,
        'title': 'Daily Discussion - ',
        # 'before': '30d', 'after': '2y', todo use these to query all posts.
    }
    response = requests.get(url, params)

    #  TODO error handling?

    # Parse data.
    data = response.json()['data']
    df = pd.DataFrame(data)

    # Clean data.
    df = clean_submission_data(df)

    if dates:
        df = filter_existing_submissions(df, dates)

    return df


def clean_submission_data(df):
    # Filter for specific columns from the data.
    column_filter = ['id', 'title']
    df = df[column_filter]

    # Filter related search results.
    deleted_filter = df.title.str.startswith('Daily Discussion -')
    df = df[deleted_filter]

    # Add date column from title string.
    df['date'] = pd.to_datetime(df.title, format='Daily Discussion - %B %d, %Y (GMT+0)')

    return df


def process_date(title):
    text_list = title.split(' ')
    filtered_text_list = text_list[3:6]
    date_string = ' '.join(filtered_text_list)

    return date_string


def get_comments(submission_id):
    # Request all comments from submission.
    url = 'https://api.pushshift.io/reddit/comment/search'
    params = {'link_id': submission_id, 'limit': 100000}
    response = requests.get(url, params)

    #  TODO error handling?

    # Parse data.
    data = response.json()['data']

    if not data:
        return None

    df = pd.DataFrame(data)

    # Clean data.
    df = clean_data(df)

    return df


def clean_data(df):
    # Filter for specific columns from the data.
    column_filter = ['body', 'created_utc', 'score', 'total_awards_received']
    df = df[column_filter]

    # Filter deleted comments from data.
    deleted_filter = df.body != '[deleted]'
    df = df[deleted_filter]

    return df


def sentiment_analysis(df):
    # Get a generator that will analyse each text string.
    pipe_generator = nlp.pipe(df.body)

    # Extract subjectivity and polarity values from nlp generator.
    nlp_values = [(doc._.subjectivity, doc._.polarity) for doc in pipe_generator]
    nlp_values_df = pd.DataFrame(nlp_values, columns=['subjectivity', 'polarity'])

    # Join nlp values to original dataframe.
    df = pd.concat([df, nlp_values_df.set_index(df.index)], axis=1)

    return df


def process_submission(submission_id):
    df = get_comments(submission_id)

    if df is None:
        return None

    df = sentiment_analysis(df)
    subjectivity = df.subjectivity.mean()

    return subjectivity


def process_submissions(df):
    submission_data = []

    for idx in df.index:

        row = df.loc[idx]

        date = row.date
        sentiment = process_submission(row.id)

        if sentiment is None:
            continue

        submission_data.append((date, sentiment))

    return submission_data


def get_new_data(dates):

    df = get_submissions(dates)
    data = process_submissions(df)

    return data