import unittest
from unittest.mock import patch
from backend.backend import Educator, DBMS, Tournament, Battle, Badge
import pandas as pd

class TestBattleClass(unittest.TestCase):
    def setUp(self):
        
        self.bid = 1
        self.battle = Battle(self.bid)
        self.battle_data = {}
    
    def test_init(self):
        self.assertEqual(self.battle.bid, self.bid)
        self.assertIsInstance(self.battle.DBMS, DBMS)
        self.assertEqual(self.battle_data, {})
    
    @patch.object(DBMS, 'read')
    def test_get_groups(self, mock_dbms_read):
        # Set up mock data for testing
        mockdf_groups = pd.DataFrame()
        
        mock_dbms_read.side_effect = [
            mockdf_groups
        ]
        # call method for testing
        self.battle.get_groups()
        
        # assert the result
        self.assertIsNotNone(self.battle.groups)
        
    
    
    '''
    def test_create_battle(self):
    
   
    @patch.object(DBMS, 'read')
    def test_get_group_submissions(self, mock_dbms_read):
        # Set up mock data for testing
        mockdf_submissions = pd.DataFrame()
        
        mock_dbms_read.side_effect = [
            mockdf_submissions
        ]
        
        user_aff = 'user_affiliation'
        # call method for testing
        self.battle.get_group_submissions(user_aff)
        
        # assert the result
        self.assertIsNotNone(mockdf_submissions)
    '''
    
    
    @patch.object(DBMS, 'read')
    def test_get_user_affiliations(self, mock_dbms_read):
        # Set up mock data for testing
        uid = 1
        mockdf_is_educator = pd.DataFrame({"is_educator": ["true"]})
        mockdf_group = pd.DataFrame({"group": ["my_group"]})
        
        mock_dbms_read.side_effect = [
            mockdf_is_educator,
            mockdf_group
        ]
        
        result = self.battle.get_user_affiliations(uid)
        
        self.assertNotEqual(result, {}) 
        self.assertEqual(result['is_educator'], 'true')  

    '''    
    @patch.object(Battle, 'get_user_affiliations')
    @patch.object(Battle, 'get_group_submissions')
    @patch.object(Battle, 'get_participants')
    @patch.object(DBMS, 'read')
    def test_get_battle_page_info(self, mock_read, mock_get_participants, mock_get_group_submissions, mock_get_user_affiliations):
        # Mocking necessary data
        mock_bid = 123  # Example battle ID
        mock_uid = 456  # Example user ID
        mock_battle_data_df = {"battle_name": "Mock Battle Name", "battle_description": "Mock Battle Description", "github_repo": "Mock GitHub Repo"}
        mock_group_submissions = {"mock_submission_data": "Mock Submission Data"}
        mock_participants = {"mock_participant_data": "Mock Participant Data"}

        # Set up mock return values for mocked methods
        mock_read.side_effect = [mock_battle_data_df, mock_group_submissions]
        mock_get_participants.return_value = mock_participants
        mock_user_aff = {"is_educator": False, "group_affiliation": {"mock_group_affiliation_data": "Mock Group Affiliation Data"}}
        mock_get_user_affiliations.return_value = mock_user_aff
        mock_get_group_submissions.return_value = mock_group_submissions

        # Instantiate Battle object
        battle = Battle(mock_bid)

        # Call the method under test
        battle.get_battle_page_info(mock_uid)

        # Assert that methods were called with the correct arguments
        mock_read.assert_called_with("GET_BATTLE_PAGE_INFO", {"_BATTLE_ID_": mock_bid})
        mock_get_user_affiliations.assert_called_with(mock_uid)
        mock_get_group_submissions.assert_called_with(mock_user_aff)
        mock_get_participants.assert_called_once()

        # Assert that battle_data attribute is correctly set
        expected_battle_data = {
            "battle_name": mock_battle_data_df["battle_name"],
            "battle_descriptions": mock_battle_data_df["battle_description"],
            "battle_repo": mock_battle_data_df["github_repo"],
            "battle_rankings": battle.battle_rankings,  # Assuming battle_rankings is set elsewhere
            "submissions": mock_group_submissions
        }
        self.assertEqual(battle.battle_data, expected_battle_data)
'''   


        
    '''   
    @patch.object(DBMS, 'read')
    def test_get_battle_page_info(self, mock_dbms_read):    
       # Set up mock data for testing
        uid = 1
        mockdf_battle_data_df = pd.DataFrame({"battle_name": ["TestBattle"],
                                              "battle_description": ["some_battle_description"],
                                              "github_repo": ["some_github_repo"]})
        mockdf_battle_rankings = pd.DataFrame()
        user_affiliations = ({'is_educator': True})
        group_submissions = 'some_group_submissions'
        participants = 'some_participants'
        
        mock_dbms_read.return_value = mockdf_battle_data_df
        
        with patch.object(Battle, 'get_user_affiliations', return_value = user_affiliations) as mock_get_user_affiliations:
            # call the method
            result_aff = self.battle.get_battle_page_info(uid)
        
        with patch.object(Battle, 'get_group_submissions', return_value = group_submissions) as mock_get_group_submissions:
            # call the method
            result_subm = self.battle.get_battle_page_info(uid)
        
        mock_dbms_read.return_value = mockdf_battle_rankings   
        
        with patch.object(Battle, 'get_groups') as mock_get_groups:
            # call the method
            result_groups = self.battle.get_battle_page_info(uid)
        
        with patch.object(Battle, 'get_participants', return_value = participants) as mock_get_participants:
            # call the method
            result_groups = self.battle.get_battle_page_info(uid)
        
        
        self.assertEqual(self.battle.battle_data["battle_name"], "TestBattle")
        self.assertEqual(self.battle.battle_data["battle_description"], "some_battle_description")
        self.assertEqual(self.battle.battle_data["github_repo"], "some_github_repo")
'''


#    def test_join(self):
       
        

    @patch.object(DBMS, 'read')
    def test_get_unassigned_subscribers(self, mock_dbms_read):
        # mock data for testing
        mockdf_unassigned_subs = pd.DataFrame({"sub_name": ["some_subscriber"]})
        
        mock_dbms_read.return_value = mockdf_unassigned_subs
        
        self.battle.get_unassigned_subscribers()
        
        # assert the results
        self.assertFalse(self.battle.unassigned_subs.empty)

        
    
  
if __name__ == '__main__':
    unittest.main()