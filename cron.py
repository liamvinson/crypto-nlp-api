import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from data_scraper import process_submissions, get_submissions
from database import insert_data
from app import db


sched = BlockingScheduler()


print('Starting cron scheduler.')


@sched.scheduled_job('interval', minutes=30)
def timed_job():
    print('Running crypto nlp update.')

    df = get_submissions([datetime.date.today()])
    data = process_submissions(df)
    insert_data(db, data)


sched.start()
