from .DataPersitenceService import DBMS
from . import GithubManagementService as GMS
from .notification_catalog import notification_catalog
from datetime import datetime



class Battle:
    def __init__(self, bid=None):
        """
        Initialize a Battle instance.

        :param bid: The battle ID, defaults to None if not provided.
        """
        self.bid = bid
        self.DBMS = DBMS()
        self.battle_data = {}



    def get_groups(self):
        if self.bid is None:
            print("Specify a battleID")
            return


        self.groups = self.DBMS.read('GET_GROUPS',{'_BATTLE_ID_':self.bid})

    def create_battle(self, battle_data):
        """
        Create a new battle in the database.

        :param battle_data: A dictionary containing data for the new battle.
        :return: 0 if the battle was created successfully, or an error message if the battle name is taken.

        The expected format of battle_data is as follows:
        # TODO: INCORPORATE THE FILES THAT ARE REQUIRED
        {
            '_BATTLE_NAME_': 'Example Battle Name',
            '_BATTLE_DESC_': 'Description of the Battle',
            '_TOURNAMENT_ID_':tid,
            '_BATTLE_REPO_': 'URL of the associated GitHub repository',
            '_BATTLE_CREATOR_': Creator's ID,
            '_END_DATE_': 'End date of the battle',
            '_REGISTRATION_DEADLINE_':'End date of registration for the battle',
            '_MIN_GROUP_SIZE_': 1,
            '_MAX_GROUP_SIZE_': 4,
            '_MANUAL_SCORING_' : boolean
        }
        """
        self.battle_data = battle_data

        # Check if the battle name is already taken
        battle_name_vacant = self.DBMS.read("BATTLE_NAME_VACANT", battle_data)[
            "count"
        ].values[0]
        if battle_name_vacant > 0:
            return "Battle Name Taken"

        # Insert the battle into the database and get its ID
        print(battle_data)
        self.bid = self.DBMS.write("CREATE_BATTLE", battle_data).fetchone()[0]
        self.battle_data["_BATTLE_ID_"] = self.bid

        # TODO: Implement GitHub integration

        return 0

    def get_group_submissions(self, user_aff):
        """
        Retrieve group submissions for a battle.

        :param user_aff: A dictionary indicating the user's affiliations.
        :return: Submissions data or a message if the user is not participating.

        The user_aff dictionary should contain:
        - 'is_educator': Boolean indicating if the user is an educator.
        - 'group_affiliation': DataFrame containing the user's group affiliation data.
        """
        if user_aff["is_educator"]:
            conditional = f"battle_id = {self.bid}"
        else:
            if user_aff["group_affiliation"].shape[0] == 0:
                return "User is not participating"

            conditional = f"battle_id = {self.bid} AND g.gid = {user_aff['group_affiliation']['gid'].values[0]}"

        submissions = self.DBMS.read("GET_SUBMISSIONS", {"_CONDITIONAL_": conditional})

        return submissions

    def get_user_affiliations(self, uid):
        """
        Get the affiliations of a user, determining if they are an educator or a student and their group affiliations.

        :param uid: User ID.
        :return: A dictionary containing the user's affiliations.
        """
        # Check if the user is an educator
        is_educator = self.DBMS.read("IS_EDUCATOR", {"_USER_ID_": uid})[
            "is_educator"
        ].values[0]

        # Retrieve the user's group affiliations
        group = self.DBMS.read(
            "GET_USER_GROUP", {"_BATTLE_ID_": self.bid, "_USER_ID_": uid}
        )

        user_affiliations = {"is_educator": is_educator, "group_affiliation": group}

        return user_affiliations
    
    def get_participants(self):
        return self.DBMS.read('GET_PARTICIPANTS',{'_BATTLE_ID_':self.bid}).values
    

    def get_battle_page_info(self, uid):
        """
        Compile information for the battle page.

        :param uid: User ID.
        :return: None. Sets various attributes of the Battle instance.
        """
        if self.bid is None:
            print("Specify a battleID")
            return
        

        # Retrieve battle information
        self.battle_data_df = self.DBMS.read(
            "GET_BATTLE_PAGE_INFO", {"_BATTLE_ID_": self.bid}
        )

        user_aff = self.get_user_affiliations(uid)

        # Retrieve relevant submissions
        self.group_submissions = self.get_group_submissions(user_aff)

        # Retrieve battle rankings
        self.battle_rankings = self.DBMS.read(
            "GET_BATTLE_RANKINGS", {"_BATTLE_ID_": self.bid}
        )

        self.get_groups()

        self.participants = self.get_participants()

        # Compile final battle information
        self.battle_data = {
            "battle_name": self.battle_data_df["battle_name"].values[0],
            "battle_descriptions": self.battle_data_df["battle_description"].values[0],
            "battle_repo": self.battle_data_df["github_repo"].values[0],
            "battle_rankings": self.battle_rankings,
            "submissions": self.group_submissions,
        }



    
    def join(self,user_ids,group_name):

        if not self.battle_data:
            self.get_battle_page_info(user_ids[0])


        
        #non_subscribed_users = self.users_subscribed_to_tournament(user_ids)
        #if len(non_subscribed_users)>0:
        #    tournament_name = self.DBMS.read("GET_TOURNAMENT_NAME",{'_TOURNAMENT_ID_':self.battle_data_df['tournament_id'].values[0]})
        #    return f"Users {', '.join(non_subscribed_users)} are not subscribed to tournament {tournament_name}"

        

        for uid in user_ids:


            # Upload to DB
            group_info = {'_GROUP_NAME_':group_name,
                        '_BATTLE_ID_':self.bid,
                            '_USER_ID_':uid}
            
            self.DBMS.write('JOIN_GROUP',group_info)

            # Register to message board

            user_name = self.DBMS.read('GET_USER_NAME_FROM_UID',{'_USER_ID_':uid})['user_name'].values[0]

            notification_info = {uid:   {"_BATTLE_NAME_":self.battle_data['battle_name'],
                                        '_USER_NAME_':user_name,
                                        '_GROUP_NAME_':group_name,
                                        '_TOURNAMENT_ID_': self.battle_data_df['tournament_id'].values[0]
                                        }
                                }

            BattleNotification = Notification("BATTLE_JOINED")

            BattleNotification.register_notfications_to_messageboard(notification_info)

    def get_unassigned_subscribers(self):
        self.unassigned_subs = self.DBMS.read('GET_UNASSIGNED_SUBSCRIBERS',{'_BATTLE_ID_':self.bid})
        return self.unassigned_subs


class Tournament:
    def __init__(self, tid=None):
        """
        Initialize a Tournament instance.

        :param tid: The tournament ID, defaults to None if not provided.
        """
        self.tid = tid
        self.DBMS = DBMS()
        self.tournament_data = {}
        

    def create_tournament(self, tournament_data):
        """
        Create a new tournament in the database.

        :param tournament_data: A dictionary containing data for the new tournament.
        :return: 'Tournament Name Taken' if the name is already in use, None otherwise.

        The tournament_data should contain the necessary information for creating a tournament.

        EXPECTED FORMAT OF THE TORUNAMENT DATA
        tournament_data = {'_TOURNAMENT_NAME_':'Tournament Name',
                            '_CREATOR_':'user_id',
                            '_DESCRIPTION_':"lorem ipsum",
                            '_SUBSCRIPTION_DEADLINE__:'yyyy-mm-dd'}
                            

        """
        self.tournament_data = tournament_data

        # Check if the tournament name is already taken
        tournament_name_vacant = self.DBMS.read(
            "TOURNAMENT_NAME_VACANT", tournament_data
        )["count"].values[0]
        if tournament_name_vacant > 0:
            return "Tournament Name Taken"

        # Insert the tournament into the database and get its ID
        self.tid = self.DBMS.write("CREATE_TOURNAMENT", tournament_data).fetchone()[0]
        self.tournament_data["_TOURNAMENT_ID_"] = self.tid

    def get_tournament_page_info(self):
        """
        Compile information for the tournament page.

        :return: None. Sets various attributes of the Tournament instance.
        """
        if self.tid is None:
            print("Specify a TournamentID")
            return

        # Retrieve tournament information
        self.tournament_data_df = self.DBMS.read(
            "GET_TOURNAMENT_PAGE_INFO", {"_TOURNAMENT_ID_": self.tid}
        )
        
        # Retrieve related battles that are ongoing
        self.related_battles_ongoing = self.DBMS.read(
            "GET_RELATED_BATTLES_ONGOING", {"_TOURNAMENT_ID_": self.tid}
        )
        
        # Retrieve related battles that are upcoming
        self.related_battles_upcoming = self.DBMS.read(
            "GET_RELATED_BATTLES_UPCOMING", {"_TOURNAMENT_ID_": self.tid}
        )


        # Retrieve tournament rankings
        self.tournament_rankings = self.DBMS.read(
            "GET_TOURNAMENT_RANKINGS", {"_TOURNAMENT_ID_": self.tid}
        )

        # Retrieve tournament badges
        self.badges = self.DBMS.read(
            "GET_TOURNAMENT_BADGES", {"_TOURNAMENT_ID_": self.tid}
        )
        
        # Retrieve all ongoing tournaments
        self.ongoing_tournaments = self.DBMS.read(
            "GET_ONGOING_TOURNAMENTS", {"_TOURNAMENT_ID_": self.tid}
        )
        
        # Retrieve all upcoming tournaments
        self.upcoming_tournaments = self.DBMS.read(
            "GET_UPCOMING_TOURNAMENTS", {"_TOURNAMENT_ID_": self.tid}
        )

        # Compile final tournament information
        self.tournament_data = {
            "tournament_name": self.tournament_data_df["tournament_name"].values[0],
            "educator_id":self.tournament_data_df["creator"].values[0],
            "related_ongoing_battles": self.related_battles_ongoing,
            "related_upcoming_battles": self.related_battles_upcoming,
            "tournament_rankings": self.tournament_rankings,
            "badges": self.badges,
        }

    def end_tournament(self):
        """
        End a tournament by updating its status in the database.

        :return: None. Updates the tournament status to indicate it has ended.
        """
        if self.tid is None:
            print("Specify a TournamentID")
            return

        # Update the tournament status to indicate it has ended
        self.DBMS.write("END_TOURNAMENT", {"_TOURNAMENT_ID_": self.tid})

        self.active = False


    def create_badge(self,badge_logic):
        badge = Badge(self.tid)

        return badge.create_badge_logic(badge_logic)


    def create_battle(self,battle_data):

        
        battle_data['_TOURNAMENT_ID_'] = self.tid
        battle_data['_BATTLE_CREATOR_'] = self.tournament_data['educator_id']

        battle = Battle()
        bid = battle.create_battle(battle_data)


    def get_notification_info(self,uid):

        user_name = self.DBMS.read('GET_USER_NAME_FROM_UID',{'_USER_ID_':uid})

        notification_info = {uid:{'_TOURNAMENT_NAME_':self.tournament_data['tournament_name'],
                             '_USER_NAME_':user_name['user_name'].values[0],
                             '_TOURNAMENT_ID_':self.tid}}
        
        return notification_info


    def subscribe(self,uid):
        self.DBMS.write("SUBSCRIBE_TO_TOURNAMENT",{'_USER_ID_':uid,
                                                   '_TOURNAMENT_ID_':self.tid})
        print('subscribe backend')
        SubscriptionNotification = Notification('SUBSCRIBED')

        notification_info = self.get_notification_info(uid)

        SubscriptionNotification.register_notfications_to_messageboard(notification_info)
        


        

    def get_affiliation(self,uid,role):
        if role == 'Educator':
            if uid == self.tournament_data['educator_id']:
                affiliation = 'Owner'
            else:
                affiliation = 'Unrelated'

        
        else:
            res = self.DBMS.read("IS_USER_SUBSCRIBED",{'_USER_ID_':uid,
                                                 '_TOURNAMENT_ID_':self.tid})
            
            if res.shape[0]>0:
                affiliation = 'Subscribed'
            else:
                affiliation = 'Not Subscribed'


        return affiliation
        



class Badge:
    def __init__(self, tid):
        """
        Initialize a Badge instance.

        :param tid: The tournament ID associated with the badge.


        The expected format of badge_data is as follows:
        {
            '_BADGE_NAME_': 'Example Badge Name' (VARCHAR),
            '_BADGE_DESC_': 'Description of the Badge' (VARCHAR),
            '_RANK_': The badge is awarded if a user places within the top _RANK_ (INT),
            '_NUM_BATTLES_': in _NUM_BATTLES_ of a tournament (INT)
        }
        """
        self.DBMS = DBMS()
        self.tid = tid

    def create_badge_logic(self, badge_logic):
        """
        Create logic for a new badge in the database.

        :param badge_logic: A dictionary containing the logic for the new badge.
        :return: None. Writes the badge logic to the database.

        The badge_logic should contain the necessary criteria for earning the badge.

        """
        badge_logic['_TOURNAMENT_ID_'] = self.tid
        # Write badge logic to the database
        self.DBMS.write("CREATE_BADGE", badge_logic)
        return 0

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
    
    def query_badge_notification_info(self,bid,uid):
        # Get badge name
        badge_name = self.DBMS.read('GET_BADGE_NAME',{'_BADGE_ID_':bid})['badge_name'].values[0]

        # get tournament info
        tournament = self.DBMS.read('GET_TOURNAMENT_NAME_FROM_BADGE_ID',{'_BADGE_ID_':bid})
        tournament_name = tournament['tournament_name'].values[0]
        tournament_id = tournament['tid'].values[0]

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


class Student:
    def __init__(self, uid):
        """
        Initialize a Student instance.

        :param uid: User ID of the student.
        """
        self.uid = uid
        self.DBMS = DBMS()
        self.tournament = None
        self.user_information = None
        self.battle = None

    def get_home_page(self):
        """
        Compile information for a student's page.

        :return: None. Retrieves and sets various attributes related to the student.
        """
        # Get tournaments
        user_tournaments = self.DBMS.read(
            "GET_USER_TOURNAMENTS", {"_USER_ID_": self.uid}
        )
        
        user_ongoing_tournaments = self.DBMS.read(
            "GET_USER_ONGOING_TOURNAMENTS", {"_USER_ID_": self.uid}
        )
        
        user_upcoming_tournaments = self.DBMS.read(
            "GET_USER_UPCOMING_TOURNAMENTS", {"_USER_ID_": self.uid}
        )
        
        user_name = self.DBMS.read('GET_USER_NAME_FROM_UID',{'_USER_ID_':self.uid})['user_name'].values[0]
    

        user_battles = self.DBMS.read("GET_USER_BATTLES", {"_USER_ID_": self.uid})
        
        user_ongoing_battles = self.DBMS.read("GET_USER_ONGOING_BATTLES", {"_USER_ID_": self.uid})

        user_upcoming_battles = self.DBMS.read("GET_USER_UPCOMING_BATTLES", {"_USER_ID_": self.uid})
        
        self.user_badges = self.DBMS.read("GET_USER_BADGES", {"_USER_ID_": self.uid})

        self.user_information = {
            "user_tournaments": user_tournaments,
            "user_ongoing_tournaments": user_ongoing_tournaments,
            "user_upcoming_tournaments": user_upcoming_tournaments,
            "user_battles": user_battles,
            "user_ongoing_battles": user_ongoing_battles,
            "user_upcoming_battles": user_upcoming_battles,
            "user_badges": self.user_badges,
            "user_name": user_name,
        }

    def get_battle_page_info(self,bid):

        self.battle = Battle(bid)

        self.battle.get_battle_page_info(self.uid)
        
        self.battle.get_unassigned_subscribers()

    def get_tournament_page_info(self,tid):

        self.tid = tid

        self.tournament = Tournament(tid)

        self.tournament.get_tournament_page_info() 

    def get_affiliation(self):

        return self.tournament.get_affiliation(self.uid,role = 'Student')
    
    
    def subscribe(self):
        print('Student subscribe')
        self.tournament.subscribe(self.uid)

    def get_studentslist(self):
        Studentlist = self.DBMS.read("GET_STUDENTS",{})
        return tuple(Studentlist['user_name']), Studentlist 


# Notification and Submission classes have been marked as placeholders and need further implementation.
class Notification:
    def __init__(self, notification_type):
        self.notification_type = notification_type
        self.DBMS = DBMS()

    def create_notification_message(self, notification_info):
        notification = notification_catalog[self.notification_type]
        for key, value in notification_info.items():
            notification = notification.replace(key, str(value))

        return notification

    def register_notfications_to_messageboard(self, notification_info):
        """
        notification_info = {1:{NOTIFICATION INFO}
                             }
        """

        for uid in notification_info.keys():
            message_string = self.create_notification_message(notification_info[uid])
            self.DBMS.write(
                "REGISTER_NOTIFICATION",
                {
                    "_USER_ID_": uid,
                    "_NOTIFICATION_TYPE_": self.notification_type,
                    "_NOTIFICATION_TEXT_": message_string,
                    "_TOURNAMENT_ID_": notification_info[uid]["_TOURNAMENT_ID_"],
                    "_BATTLE_ID_": "NULL",
                },
            )

    




class Submission:
    def __init__(self,sid):
        self.DBMS = DBMS()
        self.sid = sid

    def get_submission_info(self):
        pass

    def get_notification_info(self):
        pass #_USER_NAME_ _BATTLE_NAME_




class Educator:
    def __init__(self,uid):
        self.DBMS = DBMS()
        self.uid = uid


    def get_home_page(self):
        """
        Compile information for a student's page.

        :return: None. Retrieves and sets various attributes related to the student.
        """
        # Get tournaments
        user_tournaments = self.DBMS.read(
            "GET_EDUCATOR_TOURNAMENTS", {"_USER_ID_": self.uid}
        )
        
        user_ongoing_tournaments = self.DBMS.read(
            "GET_ONGOING_EDUCATOR_TOURNAMENTS", {"_USER_ID_": self.uid}
        )
        
        user_upcoming_tournaments = self.DBMS.read(
            "GET_UPCOMING_EDUCATOR_TOURNAMENTS", {"_USER_ID_": self.uid}
        )

        user_battles = self.DBMS.read("GET_EDUCATOR_BATTLES", {"_USER_ID_": self.uid})

        user_ongoing_battles = self.DBMS.read("GET_ONGOING_EDUCATOR_BATTLES", {"_USER_ID_": self.uid})
        
        user_upcoming_battles = self.DBMS.read("GET_UPCOMING_EDUCATOR_BATTLES", {"_USER_ID_": self.uid})
        
        user_name = self.DBMS.read("GET_USER_NAME_FROM_UID", {"_USER_ID_": self.uid})['user_name'].values[0]

        self.user_information = {
            "user_tournaments": user_tournaments,
            "user_ongoing_tournaments": user_ongoing_tournaments,
            "user_upcoming_tournaments": user_upcoming_tournaments,
            "user_battles": user_battles,
            "user_ongoing_battles": user_ongoing_battles,
            "user_upcoming_battles": user_upcoming_battles,
            "user_name": user_name
        }

    def create_battle(self,battle_data):
        current_tournament = Tournament(battle_data['_TOURNAMENT_ID_'])
        current_tournament.get_tournament_page_info()

        battle_id = current_tournament.create_battle(battle_data)

        self.battle = Battle(battle_id)

        return 0
    
    def create_tournament(self,tournament_data):
        new_tournament = Tournament()

        tournament_data['_CREATOR_'] = self.uid

        new_tournament.create_tournament(tournament_data)

        self.tournament_page_info = new_tournament.get_tournament_page_info()

        return self.tournament_page_info

    def assign_manual_score(self,score_info):
        # TODO : ISSUES WITH IDENTIFYING PRECISE SUBMISSIONS
        """
        {"_BATTLE_ID_":bid,
         "_GROUP_ID_":gid,
         "_SCORE_":score}
        """
        # update the submission entry
        self.DBMS.write("ASSIGN_MANUAL_SCORE",score_info)

        # send a notification       

        ScoredSubmission = Submission(score_info["sid"])

        notification_info = ScoredSubmission.get_notification_info()
        
        SubmissionScoredNotification = Notification('SUBMISSION_SCORED') 

        SubmissionScoredNotification.register_notfications_to_messageboard(notification_info)
        

    def end_tournament(self,tid):
        T = Tournament(tid)
        T.end_tournament()


    def create_badge(self,tid,badge_logic):
        T = Tournament(tid)
        return T.create_badge(badge_logic)
    

    def get_battle_page_info(self,bid):

        self.battle = Battle(bid)

        self.battle.get_battle_page_info(self.uid)

        self.battle.get_unassigned_subscribers()


    def get_tournament_page_info(self,tid):

        self.tid = tid

        self.tournament = Tournament(tid)

        self.tournament.get_tournament_page_info()

    def get_affiliation(self):

        return self.tournament.get_affiliation(self.uid,role = 'Educator')
    

    def get_tournaments(self):
        self.DBMS.read("GET_EDUCATOR_TOURNAMENTS",self.uid)

    def get_submission(self,smid):
        return self.DBMS.read('GET_SUBMISSIONS',{'_CONDITIONAL_':f"smid = {str(smid)}"})


    def score_submission(self,score,smid):
        self.DBMS.write('ASSIGN_MANUAL_SCORE',{'_SCORE_':score,
                                               '_SUBMISSION_ID_':smid})
    def get_studentslist(self):
        Studentlist = self.DBMS.read("GET_STUDENTS",{})
        return tuple(Studentlist['user_name']), Studentlist 
    

class Authentication_info:
    def __init__(self):
        self.DBMS = DBMS()
    
    def get_credentials(self):
        df = self.DBMS.read("GET_CREDENTIALS",{})
        # Transform the DataFrame to the desired dictionary format
        user_dict = {}
        for _, row in df.iterrows():
            username = row['user_name']
            user_dict[username] = {
                'email': row['user_email'],
                'id': row['uid'],
                'logged_in': False,  # Assuming default value as False
                'name': username,
                'password': row['password'],
                'role': 'Educator' if row['is_educator'] else 'Student'
            }

        # The final dictionary
        formatted_dict = {'usernames': user_dict}
        
        return formatted_dict
    
    def get_max_id(self):
        return self.DBMS.read("GET_MAX_ID",{}).iloc[0].values[0]

    def add_user(self, user_dict:dict):
        print(user_dict)
        self.DBMS.write("ADD_USER", {
        "_uid_": "DEFAULT", 
        "_create_date_": "CURRENT_DATE",
        "_user_email_": user_dict['email'],
        "_user_name_": user_dict['user_name'],
        "_password_": user_dict['password'],
        "_is_educator_": user_dict['role'] == 'Educator',
        "_github_": user_dict['github']
            })
    def get_uid(self, username):
        if username != '':
            return self.DBMS.read("GET_ID", {"_USER_NAME_":username}).iloc[0, 0] 
        else:
            return ''
if __name__ == "__main__":
    pass
