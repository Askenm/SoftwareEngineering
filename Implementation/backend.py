from DataPersitenceService import DBMS
import GithubManagementService as GMS

class Battle:
    def __init__(self, bid=None):
        """
        Initialize a Battle instance.

        :param bid: The battle ID, defaults to None if not provided.
        """
        self.bid = bid
        self.DBMS = DBMS()

    def create_battle(self, battle_data):
        """
        Create a new battle in the database.

        :param battle_data: A dictionary containing data for the new battle.
        :return: 0 if the battle was created successfully, or an error message if the battle name is taken.

        The expected format of battle_data is as follows:
        {
            '_BATTLE_NAME_': 'Example Battle Name',
            '_BATTLE_DESC_': 'Description of the Battle',
            '_BATTLE_REPO_': 'URL of the associated GitHub repository',
            '_BATTLE_CREATOR_': Creator's ID,
            '_END_DATE_': 'End date of the battle'
        }
        """
        self.battle_data = battle_data

        # Check if the battle name is already taken
        battle_name_vacant = self.DBMS.read("BATTLE_NAME_VACANT", battle_data)["count"].values[0]
        if battle_name_vacant > 0:
            return "Battle Name Taken"

        # Insert the battle into the database and get its ID
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
        is_educator = self.DBMS.read("IS_EDUCATOR", {"_USER_ID_": uid})["is_educator"].values[0]

        # Retrieve the user's group affiliations
        group = self.DBMS.read("GET_USER_GROUP", {"_BATTLE_ID_": self.bid, "_USER_ID_": uid})

        user_affiliations = {"is_educator": is_educator, "group_affiliation": group}

        return user_affiliations

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
        self.battle_data_df = self.DBMS.read("GET_BATTLE_PAGE_INFO", {"_BATTLE_ID_": self.bid})

        user_aff = self.get_user_affiliations(uid)

        # Retrieve relevant submissions
        self.group_submissions = self.get_group_submissions(user_aff)

        # Retrieve battle rankings
        self.battle_rankings = self.DBMS.read("GET_BATTLE_RANKINGS", {"_BATTLE_ID_": self.bid})

        # Compile final battle information
        self.battle_data = {
            "battle_name": self.battle_data_df["battle_name"].values[0],
            "battle_descriptions": self.battle_data_df["battle_description"].values[0],
            "battle_repo": self.battle_data_df["github_repo"].values[0],
            "battle_rankings": self.battle_rankings,
            "submissions": self.group_submissions,
        }

# The following classes (Tournament, Notification, Submission, Badge, Student) follow a similar structure.
# They are initialized with relevant IDs or settings, and contain methods to interact with the database (DBMS)
# and perform specific actions like creating tournaments, handling badges, etc.
# Each method should be documented similarly, explaining its purpose, parameters, return values, and any side effects.

if __name__ == "__main__":
    pass



class Tournament:
    def __init__(self, tid=None):
        """
        Initialize a Tournament instance.

        :param tid: The tournament ID, defaults to None if not provided.
        """
        self.tid = tid
        self.DBMS = DBMS()

    def create_tournament(self, tournament_data):
        """
        Create a new tournament in the database.

        :param tournament_data: A dictionary containing data for the new tournament.
        :return: 'Tournament Name Taken' if the name is already in use, None otherwise.

        The tournament_data should contain the necessary information for creating a tournament.
        """
        self.tournament_data = tournament_data

        # Check if the tournament name is already taken
        tournament_name_vacant = self.DBMS.read("TOURNAMENT_NAME_VACANT", tournament_data)["count"].values[0]
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
        self.tournament_data_df = self.DBMS.read("GET_TOURNAMENT_PAGE_INFO", {"_TOURNAMENT_ID_": self.tid})

        # Retrieve related battles
        self.related_battles = self.DBMS.read("GET_RELATED_BATTLES", {"_TOURNAMENT_ID_": self.tid})

        # Retrieve tournament rankings
        self.tournament_rankings = self.DBMS.read("GET_TOURNAMENT_RANKINGS", {"_TOURNAMENT_ID_": self.tid})

        # Retrieve tournament badges
        self.badges = self.DBMS.read("GET_TOURNAMENT_BADGES", {"_TOURNAMENT_ID_": self.tid})

        # Compile final tournament information
        self.tournament_data = {
            "tournament_name": self.tournament_data_df["tournament_name"].values[0],
            "related_battles": self.related_battles,
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


class Badge:
    def __init__(self, tid):
        """
        Initialize a Badge instance.

        :param tid: The tournament ID associated with the badge.
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
        # Write badge logic to the database
        self.DBMS.write('CREATE_BADGE', badge_logic)

    def assign_badge(self, uid, bid):
        """
        Assign a badge to a user.

        :param uid: User ID.
        :param bid: Badge ID.
        :return: None. Awards the badge to the specified user.
        """
        # Award the badge to the user
        self.DBMS.write("AWARD_BADGE", {"_USER_ID_": uid, "_BADGE_ID_": bid})

    def check_badge_achievers(self, bid):
        """
        Check and assign badges to eligible users based on badge criteria.

        :param bid: Badge ID.
        :return: None. Assigns badges to users who meet the criteria.
        """
        # Get badge logic
        badge_logic_df = self.DBMS.read('GET_BADGE_LOGIC', {'_BADGE_ID_': bid})

        badge_logic = {'_TOURNAMENT_ID_': badge_logic_df['tournament_id'].values[0],
                       '_RANK_': badge_logic_df['rank'].values[0],
                       '_NUM_BATTLES_': badge_logic_df['num_battles'].values[0]}
        
        # Get all potential badge achievers
        badge_achievers = self.DBMS.read("GET_BADGE_ACHIEVERS", badge_logic)['uid'].values
        
        # Get current badge holders
        existing_badge_achievers = self.DBMS.read("GET_CURRENT_BADGE_HOLDERS", {'_BADGE_ID_': bid})['uid'].values

        # Determine new badge awardees
        new_awardees = set(badge_achievers) - set(existing_badge_achievers)
        for _uid in new_awardees:
            self.assign_badge(_uid, bid)
            # TODO: Implement notification system

class Student:
    def __init__(self, uid):
        """
        Initialize a Student instance.

        :param uid: User ID of the student.
        """
        self.uid = uid

    def get_student_page(self):
        """
        Compile information for a student's page.

        :return: None. Retrieves and sets various attributes related to the student.
        """
        # TODO: Implement functionality to retrieve tournaments, battles, and badges for the student

# Notification and Submission classes have been marked as placeholders and need further implementation.
class Notification:
    def __init__(self):
        pass

class Submission:
    def __init__(self):
        pass

if __name__ == "__main__":
    pass