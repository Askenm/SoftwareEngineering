import schedule
import time
from handlers import NotificationHandler, BadgeHandler, SubmissionHandler

def job():
    # Badges
    print("Checking for Badges...")
    BH = BadgeHandler()
    BH.check_for_badges()

    # Submissions
    print("Checking for submissions...")
    SH = SubmissionHandler()
    SH.check_for_submissions()

    # Notifications
    print("Checking for notifications...\n\n")
    NH = NotificationHandler()
    NH.check_for_notifications()




    

# Schedule the job
schedule.every(1).minute.do(job)

# Loop so that the scheduling task runs continuously
while True:
    schedule.run_pending()
    time.sleep(1)  # Wait for one second
