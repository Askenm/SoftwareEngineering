import unittest
from unittest.mock import patch
from backend.backend import Educator, DBMS, Tournament, Battle, Badge
import pandas as pd


class TestTournamentClass(unittest.TestCase):
    def setUp(self):
        
        self.tid = 1
        self.tournament = Tournament(self.tid)
        self.tournament_data = {}
    
    def test_init(self):
        self.assertEqual(self.tournament.tid, self.tid)
        self.assertIsInstance(self.tournament.DBMS, DBMS)
        self.assertEqual(self.tournament_data, {})
    
    
    @patch('backend.backend.DBMS.read')
    @patch('backend.backend.DBMS.write')
    def test_create_tournament(self, mock_dbms_write, mock_dbms_read):
        # Initialize a test tournament data
        tournament_data = pd.DataFrame({
            '_TOURNAMENT_NAME_': ['Test Tournament'],
            '_CREATOR_': ['test_user_id'],
            '_DESCRIPTION_': ['lorem ipsum'],
            '_SUBSCRIPTION_DEADLINE__': ['yyyy-mm-dd']
        })
        
        # Mock the DBMS.write method to return the tournament ID
        mock_dbms_write.return_value.fetchone.return_value = (1,)
        
        # Mock the DBMS.read method to return 0 for tournament name not taken
        mock_dbms_read.return_value = pd.DataFrame({'count': [0]})
        
        # Call the method to be tested
        self.tournament.create_tournament(tournament_data)
        
        # Assert that DBMS.read was called with the correct arguments
        mock_dbms_read.assert_called_once_with("TOURNAMENT_NAME_VACANT", tournament_data)
        
        # Assert that DBMS.write was called with the correct arguments
        expected_write_args = ("CREATE_TOURNAMENT", tournament_data)
        mock_dbms_write.assert_called_once_with(*expected_write_args)
        
        # Assert that the tournament ID was set correctly
        self.assertEqual(self.tid, 1)
        self.assertEqual(self.tournament.tournament_data.get("_TOURNAMENT_ID_").item(), 1)

      
    @patch.object(DBMS, 'read')
    def test_get_tournament_page_info(self, mock_dbms_read):
            
         # Set up mock data for testing
        mockdf_tournament_data = pd.DataFrame({"tournament_name": ["tournament 1"],
                                               "creator": ["educatorId"]})
        mockdf_related_battles_ongoing = pd.DataFrame()
        mockdf_related_battles_upcoming = pd.DataFrame()
        mockdf_tournament_rankings = pd.DataFrame()
        mockdf_badges = pd.DataFrame()
        mockdf_ongoing_tournaments = pd.DataFrame()
        mockdf_upcoming_tournaments = pd.DataFrame()
        
        mock_dbms_read.side_effect = [
            mockdf_tournament_data,
            mockdf_related_battles_ongoing,
            mockdf_related_battles_upcoming,
            mockdf_tournament_rankings,
            mockdf_badges,
            mockdf_ongoing_tournaments,
            mockdf_upcoming_tournaments,
        ]
        
        # Call the method to test
        self.tournament.get_tournament_page_info()

        # Assert the results
        # test that the correct df fetched from the db is assigned to the correct key in the tournament_data object dicionary
        
        self.assertEqual(self.tournament.tournament_data["tournament_name"], "tournament 1")
        self.assertEqual(self.tournament.tournament_data["educator_id"], "educatorId")
        self.assertIs(self.tournament.tournament_data["related_ongoing_battles"], mockdf_related_battles_ongoing)
        self.assertIs(self.tournament.tournament_data["related_upcoming_battles"], mockdf_related_battles_upcoming)
        self.assertIs(self.tournament.tournament_data["tournament_rankings"], mockdf_tournament_rankings)
        self.assertIs(self.tournament.tournament_data["badges"], mockdf_badges)
    
    '''
    @patch('backend.backend.DBMS')
    def test_end_tournament(self, mock_DBMS):
        # Create a mock object for the DBMS
        
       # return_value.fetchone.return_value = None
       
        mock_dbms_instance = mock_DBMS.return_value
        mock_dbms_instance.write = lambda *args, **kwargs: None
        mock_dbms_instance.write.return_value = None

        # Set the tournament ID
      #  self.tournament.tid = 1

        # Call the end_tournament method
        self.tournament.end_tournament()

        # Assert that the tournament ID is set correctly
        self.assertEqual(self.tournament.tid, 1)

        # Assert that the correct parameters were passed to the DBMS write method
        mock_dbms_instance.write.assert_called_once_with("END_TOURNAMENT", {"_TOURNAMENT_ID_": 1})
'''
    
    
        
    def test_create_badge(self):
        # set up mock data for testing
        some_badge_logic = 'some_badge_logic' 
            
        with patch.object(Badge, 'create_badge_logic') as mock_create_badge:
                self.tournament.create_badge(some_badge_logic)
        
        mock_create_badge.assert_called_with(some_badge_logic)
    
    '''
    @patch('backend.backend.DBMS')
    def test_create_battle(self, mock_dbms):
        # Mock data
        tournament_data = pd.DataFrame({'educator_id': [2],'_TOURNAMENT_ID_': [], '_TOURNAMENT_NAME_': ['Test Tournament']})
        battle_data = pd.DataFrame ({'_BATTLE_CREATOR_':[], 'educator': [],'_BATTLE_NAME': ['test']})  

        # Mock DBMS methods
        mock_dbms_instance = mock_dbms.return_value
        mock_dbms_instance.write.return_value.fetchone.return_value = (123,)  # Mock battle ID
        
        # Create a tournament instance
        tournament = Tournament(tournament_data['_TOURNAMENT_ID_'])

        # Call the create_battle method
        with patch.object(Battle, 'create_battle') as mock_create_battle:
            tournament.create_battle(battle_data)

        # Assert that the DBMS write method was called with the correct arguments
        expected_write_args = {'_TOURNAMENT_ID_': tournament_data['_TOURNAMENT_ID_'], '_BATTLE_NAME_': 'Test Battle', '_CREATOR_': 1}
        mock_dbms_instance.write.assert_called_once_with('CREATE_BATTLE', expected_write_args)

        # Assert that Battle.create_battle was called with the correct arguments
        mock_create_battle.assert_called_once_with(battle_data)
        
           
    def test_create_battle(self):
        # Mocking necessary data
        self.tournament_data = {'educator_id': 1}
        
        battle_data = {
            '_TOURNAMENT_ID_': 1,
            '_BATTLE_CREATOR_': self.tournament_data['educator_id'],
        }
        someBattleId = 17
        
        # Mocking the create_battle method of the Tournament class
        with patch.object(Battle, 'create_battle', return_value=someBattleId) as mock_create_battle:
            result = self.tournament.create_battle(battle_data)
        
        # Asserting that the expected methods were called
    #    self.assertEqual(self.tournament.battle.bid, someBattleId)
        self.assertEqual(result, 0)
        mock_create_battle.assert_called_with(battle_data)
      
    @patch.object(DBMS, 'read')   
    def test_get_notification_info(self, mock_dbms_read):
        # Set up mock data for testing
        uid = 1
        mockdf_user_name = pd.DataFrame({"user_name": ["John Doe"]})
        mock_notification_info = 'some_notification_info' 
        
        mock_dbms_read.side_effect = [
                mockdf_user_name
        ]
        
        result = self.tournament.get_notification_info(uid)
        
        self.assertListEqual(result, mock_notification_info)
      

    def test_subsribe(self):


    def test_get_affiliation(self):
            
'''             
            



if __name__ == '__main__':
    unittest.main()