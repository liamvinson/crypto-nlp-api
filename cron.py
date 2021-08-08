from data_scraper import process_submission
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


print('Starting cron scheduler.')


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

    res = process_submission('oxgbs8')
    print(res)


sched.start()
