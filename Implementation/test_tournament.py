import unittest
from unittest.mock import patch
from backend.backend import Educator, DBMS, Tournament, Battle, Badge
import pandas as pd


#self.educator.DBMS.write.assert_called_with('END_TOURNAMENT', {"_TOURNAMENT_ID_": tournament_id})

class TestTournamentClass(unittest.TestCase):
    def setUp(self):
        
        self.tid = 1
        self.tournament = Tournament(self.tid)
        self.tournament_data = {}
    
    def test_init(self):
        self.assertEqual(self.tournament.tid, self.tid)
        self.assertIsInstance(self.tournament.DBMS, DBMS)
        self.assertEqual(self.tournament_data, {})

        '''
    @patch.object(DBMS, 'write')
    def test_create_tournament(self, mock_dbms_write):
        # Mocking necessary data    
        some_tournament_data = {
            '_TOURNAMENT_ID_': 1,
            '_TOURNAMENT_CREATOR_': 'example_creator_id',
        }
        someTournamentId = 1
        
        mock_dbms_write.side_effects = [
                ("CREATE_TOURNAMENT", some_tournament_data)
        ]
        
        self.tournament.create_tournament(some_tournament_data)
        
        assert
        '''        
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
    
        
    def test_create_badge(self):
        # set up mock data for testing
        some_badge_logic = 'some_badge_logic' 
            
        with patch.object(Badge, 'create_badge_logic') as mock_create_badge:
                self.tournament.create_badge(some_badge_logic)
        
        mock_create_badge.assert_called_with(some_badge_logic)
        
        '''   
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