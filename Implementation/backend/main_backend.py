import schedule
import time
from .handlers import NotificationHandler, BadgeHandler, SubmissionHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback

# Email configuration
sender_email = "codekatabattles@gmail.com" # Replace with your email address
receiver_email = "aske.osv@gmail.com"  # Replace with the email address to receive the error reports
password = "vjxq xdrl xevv gimb"  # Replace with your email password
smtp_server = "smtp.example.com"  # Replace with your SMTP server
smtp_port = 587  # SMTP port number, for Gmail it's 587

def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))


    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()  # Enable security
        smtp.login(sender_email, password)  # Login with email and password
        text = message.as_string()
        smtp.sendmail(sender_email, receiver_email, message.as_string())

def job():
    # Badges
    try:
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



    except Exception as e:
        error_message = traceback.format_exc()
        print("An error occurred, sending email...")
        send_email("Job Script Failed", error_message)




    

# Schedule the job
schedule.every(1).minute.do(job)

# Loop so that the scheduling task runs continuously
while True:
    schedule.run_pending()
    time.sleep(1)  # Wait for one second
