import schedule
import time
from handlers import NotificationHandler, BadgeHandler

def job():
    # Badges
    print("Checking for Badges...")
    BH = BadgeHandler()
    BH.check_for_badges()

    # Notifications
    print("Checking for notifications...")
    NH = NotificationHandler()
    NH.check_for_notifications()


    

# Schedule the job
schedule.every(1).minute.do(job)

# Loop so that the scheduling task runs continuously
while True:
    schedule.run_pending()
    time.sleep(1)  # Wait for one second
