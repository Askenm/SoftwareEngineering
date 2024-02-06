import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


from .DataPersitenceService import DBMS
from .backend import Notification


class NotificationHandler:
    def __init__(self):
        """
        Initialize the NotificationHandler instance.
        """
        self.DBMS = DBMS()  # Instance of the Database Management System

        # Email credentials for sending notifications
        self.sender_email = "codekatabattles@gmail.com"
        self.sender_password = "vjxq xdrl xevv gimb"  # Use app-specific password

    def check_for_notifications(self):
        """
        Check the database for any pending notifications and send them.
        """
        pending_notifications = self.DBMS.read("CHECK_MESSAGEBOARD", {})
        if pending_notifications.shape[0] > 0:
            self.send_pending_notifications(pending_notifications)

    def structure_notificaiton_information_from_db_row(self, row):
        """
        Extract notification information from a database row.

        :param row: A row from the database representing a notification.
        :return: A dictionary containing structured notification information.
        """
        notification_info = {
            'recipient_email': row['user_email'],
            'notification_id': row['nid'],
            'notification_type': row['notification_type'],
            'notification_text': row['notification_text']
        }
        
        return notification_info

    def send_pending_notifications(self, pending_notifications):
        """
        Send all pending notifications.

        :param pending_notifications: DataFrame containing pending notifications.
        """
        for rownum, row in pending_notifications.iterrows():
            notification_info = self.structure_notificaiton_information_from_db_row(row)
            self.send_notification(notification_info)

    def mark_notification_as_sent(self, notification_info):
        """
        Mark a notification as sent in the database.

        :param notification_info: Dictionary containing information about the notification.
        """
        self.DBMS.write('MARK_NOTIFICATION_AS_SENT', {'_NOTIFICATION_ID_': notification_info['notification_id']})

    def send_notification(self, notification_info):
        """
        Send a notification email.

        :param notification_info: Dictionary containing information about the notification to be sent.
        """
        # Setting up the MIME for the email
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = notification_info["recipient_email"]
        message['Subject'] = notification_info["notification_type"].replace('_', ' ')
        message.attach(MIMEText(notification_info["notification_text"], 'plain'))

        # Sending the email using SMTP session
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()  # Enable security
                smtp.login(self.sender_email, self.sender_password)  # Login with email and password
                text = message.as_string()
                smtp.sendmail(self.sender_email, notification_info["recipient_email"], text)

            # Marking the notification as sent after successful email sending
            self.mark_notification_as_sent(notification_info)

        except Exception as e:
            print(f"Error: {e}")




class BadgeHandler:
    def __init__(self):
        self.DBMS = DBMS()


    def check_for_badges(self):
        all_badges = self.DBMS.read("GET_ALL_BADGES",{})
        for bid in all_badges['bid'].values:
            self.check_badge_achievers(bid)


    def assign_badge(self, uid, bid):
        """
        Assign a badge to a user.

        :param uid: User ID.
        :param bid: Badge ID.
        :return: None. Awards the badge to the specified user.
        """
        # Award the badge to the user
        self.DBMS.write("AWARD_BADGE", {"_USER_ID_": uid, "_BADGE_ID_": bid})

    def get_current_date(self):
        # Get the current date
        current_date = datetime.now()

        # Format the date as yyyy-mm-dd
        formatted_date = current_date.strftime('%Y-%m-%d')

        return formatted_date
    
    def query_badge_notification_info(self,uid,bid):
        # Get badge name
        badge_name = self.DBMS.read('GET_BADGE_NAME',{'_BADGE_ID_':bid})['badge_name'].values[0]

        # get tournament info
        tournament = self.DBMS.read('GET_TOURNAMENT_NAME_FROM_BADGE_ID',{'_BADGE_ID_':bid})
        tournament_name = tournament['tournament_name'].values[0]
        tournament_id = tournament['tournament_id'].values[0]

        # get user info
        user_name = self.DBMS.read('GET_USER_NAME_FROM_UID',{'_USER_ID_':uid})['user_name'].values[0]

        notification_info = {uid:{"_BADGE_NAME_":badge_name,
                             '_USER_NAME_':user_name,
                             '_TOURNAMENT_NAME_':tournament_name,
                             '_TOURNAMENT_ID_': tournament_id,
                             '_BADGE_ACHIEVED_DATE_':self.get_current_date()}
                             }

        # return to notification
        return notification_info


    def badge_awarded_notification(self,uid,bid):

        notification_info = self.query_badge_notification_info(uid,bid)

        BadgeNotification = Notification('BADGE_ACHIEVED')

        BadgeNotification.register_notfications_to_messageboard(notification_info)


    def check_badge_achievers(self, bid):
        """
        Check and assign badges to eligible users based on badge criteria.

        :param bid: Badge ID.
        :return: None. Assigns badges to users who meet the criteria.
        """
        # Get badge logic
        badge_logic_df = self.DBMS.read("GET_BADGE_LOGIC", {"_BADGE_ID_": bid})

        badge_logic = {
            "_TOURNAMENT_ID_": badge_logic_df["tournament_id"].values[0],
            "_RANK_": badge_logic_df["rank"].values[0],
            "_NUM_BATTLES_": badge_logic_df["num_battles"].values[0],
        }

        # Get all potential badge achievers
        badge_achievers = self.DBMS.read("GET_BADGE_ACHIEVERS", badge_logic)[
            "uid"
        ].values

        # Get current badge holders
        existing_badge_achievers = self.DBMS.read(
            "GET_CURRENT_BADGE_HOLDERS", {"_BADGE_ID_": bid}
        )["uid"].values

        # Determine new badge awardees
        new_awardees = set(badge_achievers) - set(existing_badge_achievers)
        for _uid in new_awardees:
            
            # Register badge assignment in DB
            self.assign_badge(_uid, bid)

            # upload notification of badge assignment to messageboard
            self.badge_awarded_notification(_uid, bid)



class SubmissionHandler:
    def __init__(self):
        self.DBMS = DBMS()

    def check_for_submissions(self):
        new_subs = self.DBMS.read("GET_NEW_SUBMISSIONS",{})
        for row_idx,row in new_subs.iterrows():
            self.register_submission_notfications_to_messageboard(row['gid'])

            self.DBMS.write('MARK_SUBMISSION_AS_SENT',{'_SUBMISSION_ID_':row['smid']})


    def structure_badge_notification_info(self,row):
        return {row['uid'].values[0]:{'_USER_NAME_':row['user_name'],
                                      '_BATTLE_NAME_':row['battle_name'],
                                      '_BATTLE_ID_':row['bid'].values[0],
                                      '_TOURNAMENT_ID_':row['tournament_id']}}
    


    def register_submission_notfications_to_messageboard(self,gid):

        users = self.DBMS.read('GET_USERS_FROM_GID',{'_GROUP_ID_':gid})

        for rix, row in users.iterrows():
            #print(row)
            notification_info = self.structure_badge_notification_info(row)

            SubmissionNotification = Notification('NEW_SUBMISSION')

            SubmissionNotification.register_notfications_to_messageboard(notification_info)




if __name__ =='__main__':
    SH = SubmissionHandler()
    SH.check_for_submissions()