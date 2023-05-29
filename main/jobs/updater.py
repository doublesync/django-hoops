from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import auto_collect_rewards


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_collect_rewards, "interval", days=1)
    scheduler.start()
    print("Scheduler started.")
