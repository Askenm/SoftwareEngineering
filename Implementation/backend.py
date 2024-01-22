from DataPersitenceService import DBMS
import GithubManagementService as GMS

class Battle():
    def __init__(self,bid=None):
        self.bid = bid
        self.DBMS = DBMS()


    def create_battle(self,battle_data):

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

   
        # TODO
        battle_name_vacant = self.DBMS.read('BATTLE_NAME_VACANT',battle_data)['count'].values[0]
        if battle_name_vacant > 0:
            return 'Battle Name Taken'
        


        # GET BATTLE ID FROM DB
        self.bid = self.DBMS.write('CREATE_BATTLE',battle_data).fetchone()[0]
        

        # TODO
        # GITHUB SHIZNIT
        GMS.submit_battle_data(battle_data)


        return 0


        



    def get_battle_page_info(self):
        if self.bid == None:
            print('Specify a battleID')
            return
        
        # Get Battlename
        # Get Battle Description
        # Get Battle Link
        self.battle_data_df = self.DBMS.read('GET_BATTLE_PAGE_INFO',{"_BATTLE_ID_":self.bid})

        # GET BATTLE RANKINGS
        self.battle_rankings = self.DBMS.read('GET_BATTLE_RANKINGS',{"_BATTLE_ID_":self.bid})

        # CREATE FINAL INFORMATION TABLE
        self.battle_data = {"battle_name":self.battle_data_df['battle_name'].values[0],
                            "battle_descriptions":self.battle_data_df['battle_description'].values[0],
                            "battle_repo":self.battle_data_df['github_repo'].values[0],
                            "battle_rankings":self.battle_rankings}



if __name__ == '__main__':


    # Create battle test
    example = {"_BATTLE_NAME_":"'dis_battle_mon'", "_BATTLE_DESC_": "'dis_battle_mon'", "_BATTLE_REPO_":"'YADAYADA.git'", "_BATTLE_CREATOR_":1,"_END_DATE_":"'2024-08-12'"}
    Battle_ = Battle()
    #Battle_.get_battle_page_info()
    Battle_.create_battle(example)

    print(Battle_.battle_data)
        
