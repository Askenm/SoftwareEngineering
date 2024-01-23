from DataPersitenceService import DBMS
import GithubManagementService as GMS


class Battle:
    def __init__(self, bid=None):
        self.bid = bid
        self.DBMS = DBMS()

    def create_battle(self, battle_data):
        """
        EXAMPLE BATTLE_DATA
        Just fill out the values and everything will be created in the DB

        {'_BATTLE_NAME_': "'dis_battle_mon'",
        '_BATTLE_DESC_': "'dis_battle_mon'",
        '_BATTLE_REPO_': "'YADAYADA.git'",
        '_BATTLE_CREATOR_': 1,
        '_END_DATE_': "'2024-08-12'"}
        """

        self.battle_data = battle_data

        battle_name_vacant = self.DBMS.read("BATTLE_NAME_VACANT", battle_data)[
            "count"
        ].values[0]
        if battle_name_vacant > 0:
            return "Battle Name Taken"

        # GET BATTLE ID FROM DB
        self.bid = self.DBMS.write("CREATE_BATTLE", battle_data).fetchone()[0]
        self.battle_data["_BATTLE_ID_"] = self.bid

        # TODO
        # GITHUB SHIZNIT
        # GMS.submit_battle_data(battle_data)

        return 0

    def get_group_submissions(self, user_aff):
        if user_aff["is_educator"]:
            conditional = f"battle_id = {self.bid}"
        else:
            if user_aff["group_affiliation"].shape[0] == 0:
                return "User is not paticipating"

            conditional = f"battle_id = {self.bid} AND g.gid = {user_aff['group_affiliation']['gid'].values[0]}"

        submissions = self.DBMS.read("GET_SUBMISSIONS", {"_CONDITIONAL_": conditional})

        return submissions

    def get_user_affiliations(self, uid):
        # Is user educator or student
        is_educator = self.DBMS.read("IS_EDUCATOR", {"_USER_ID_": uid})[
            "is_educator"
        ].values[0]

        # What group is the user part of?
        # If educator, get all submissions
        group = self.DBMS.read(
            "GET_USER_GROUP", {"_BATTLE_ID_": self.bid, "_USER_ID_": uid}
        )

        user_affiliations = {"is_educator": is_educator, "group_affiliation": group}

        return user_affiliations

    def get_battle_page_info(self, uid):
        if self.bid == None:
            print("Specify a battleID")
            return

        # Get Battlename
        # Get Battle Description
        # Get Battle Link
        self.battle_data_df = self.DBMS.read(
            "GET_BATTLE_PAGE_INFO", {"_BATTLE_ID_": self.bid}
        )

        user_aff = self.get_user_affiliations(uid)

        # GET RELEVANT SUBMISSION
        self.group_submissions = self.get_group_submissions(user_aff)

        # GET BATTLE RANKINGS
        self.battle_rankings = self.DBMS.read(
            "GET_BATTLE_RANKINGS", {"_BATTLE_ID_": self.bid}
        )

        # CREATE FINAL INFORMATION TABLE
        self.battle_data = {
            "battle_name": self.battle_data_df["battle_name"].values[0],
            "battle_descriptions": self.battle_data_df["battle_description"].values[0],
            "battle_repo": self.battle_data_df["github_repo"].values[0],
            "battle_rankings": self.battle_rankings,
            "submissions": self.group_submissions,
        }


class Tournament:
    def __init__(self, tid=None):
        self.tid = tid
        self.DBMS = DBMS()

    def create_tournament(self, tournament_data):
        self.tournament_data = tournament_data

        tournament_name_vacant = self.DBMS.read(
            "TOURNAMENT_NAME_VACANT", tournament_data
        )["count"].values[0]
        if tournament_name_vacant > 0:
            return "Tournament Name Taken"

        # GET BATTLE ID FROM DB
        self.tid = self.DBMS.write("CREATE_TOURNAMENT", tournament_data).fetchone()[0]
        self.tournament_data["_TOURNAMENT_ID_"] = self.tid

    def get_tournament_page_info(self):
        if self.tid == None:
            print("Specify a TournamentID")
            return

        # Get Tournamentname
        self.tournament_data_df = self.DBMS.read(
            "GET_TOURNAMENT_PAGE_INFO", {"_TOURNAMENT_ID_": self.tid}
        )

        # Get related Battles
        self.related_battles = self.DBMS.read(
            "GET_RELATED_BATTLES", {"_TOURNAMENT_ID_": self.tid}
        )

        # GET BATTLE RANKINGS
        self.tournament_rankings = self.DBMS.read(
            "GET_TOURNAMENT_RANKINGS", {"_TOURNAMENT_ID_": self.tid}
        )

        # GET TOURNAMENT BADGES
        self.badges = self.DBMS.read(
            "GET_TOURNAMENT_BADGES", {"_TOURNAMENT_ID_": self.tid}
        )

        # CREATE FINAL INFORMATION TABLE
        self.tournament_data = {
            "tournament_name": self.tournament_data_df["tournament_name"].values[0],
            "related_battles": self.related_battles,
            "tournament_rankings": self.tournament_rankings,
            "badges": self.badges,
        }

    def end_tournament(self):
        if self.tid == None:
            print("Specify a TournamentID")
            return

        self.DBMS.write("END_TOURNAMENT", {"_TOURNAMENT_ID_": self.tid})


class Notification:
    def __init__(self):
        pass


class Submission:
    def __init__(self):
        pass


class Badge:
    def __init__(self):
        pass

    def create_badge_logic(self, badge_logic):
        pass

    def assign_badge(self, uid, bid):
        pass

    def check_badge_achievers(self, bid):
        pass


class Student:
    def __init__(self):
        pass

    def get_student_page(self):
        pass

    def get_student_badges(self):
        pass


if __name__ == "__main__":
    pass
