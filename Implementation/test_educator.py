import unittest
from unittest.mock import patch
from backend.backend import Educator, DBMS, Tournament, Battle
import pandas as pd

class TestEducatorClass(unittest.TestCase):
    def setUp(self):
        
        self.uid = 1
        self.educator = Educator(self.uid)
    
    def test_init(self):
        self.assertEqual(self.educator.uid, self.uid)
        self.assertIsInstance(self.educator.DBMS, DBMS)

    @patch.object(DBMS, 'read')
    def test_get_home_page(self, mock_dbms_read):
        
        # Set up mock data for testing
        mockdf_tournaments = pd.DataFrame()
        mockdf_ongoing_tournaments = pd.DataFrame()
        mockdf_upcoming_tournaments = pd.DataFrame()
        mockdf_user_name = pd.DataFrame({"user_name": ["John Doe"]})
        mockdf_battles = pd.DataFrame()
        mockdf_ongoing_battles = pd.DataFrame()
        mockdf_upcoming_battles = pd.DataFrame()
       
    

        mock_dbms_read.side_effect = [
            mockdf_tournaments,
            mockdf_ongoing_tournaments,
            mockdf_upcoming_tournaments,
            mockdf_battles,
            mockdf_ongoing_battles,
            mockdf_upcoming_battles,
            mockdf_user_name,
        ]


        # Call the method to test
        self.educator.get_home_page()

        # Assert the results
        # test that the correct df fetched from the db is assigned to the correct key in the user_information object dicionary
        self.assertIs(self.educator.user_information["user_tournaments"], mockdf_tournaments)
        self.assertIs(self.educator.user_information["user_ongoing_tournaments"], mockdf_ongoing_tournaments)
        self.assertIs(self.educator.user_information["user_upcoming_tournaments"], mockdf_upcoming_tournaments)
        self.assertEqual(self.educator.user_information["user_name"], "John Doe")
        self.assertIs(self.educator.user_information["user_battles"], mockdf_battles)
        self.assertIs(self.educator.user_information["user_ongoing_battles"], mockdf_ongoing_battles)
        self.assertIs(self.educator.user_information["user_upcoming_battles"], mockdf_upcoming_battles)
    
        
     
    def test_create_battle(self):
        # Mocking necessary data
        battle_data = {
            '_TOURNAMENT_ID_': 1,
            '_BATTLE_CREATOR_': 'example_creator_id',
        }
        someBattleId = 17
        
        # Mocking the create_battle method of the Tournament class
        with patch.object(Tournament, 'create_battle', return_value=someBattleId) as mock_create_battle:
            result = self.educator.create_battle(battle_data)
        
        # Asserting that the expected methods were called
        self.assertEqual(self.educator.battle.bid, someBattleId)
        self.assertEqual(result, 0)
        mock_create_battle.assert_called_with(battle_data)

    def test_create_tournament(self):
        # Mocking necessary data
        tournament_data = {
            '_TOURNAMENT_ID_': 1,
            '_TOURNAMENT_CREATOR_': 'example_creator_id',
        }
        
        some_tournament_page_info = {
            'tournament_name': 'test_tournament',
            'educator_id': 'example_id,'
        }
        
        # Asserting that the expected methods were called
        with patch.object(Tournament, 'create_tournament', return_value = some_tournament_page_info ) as mock_create_tournament:
            result = self.educator.create_tournament(tournament_data)
        
    #    self.assertEqual(self.educator.tournament_page_info, some_tournament_page_info)
    #    self.assertEqual(result,some_tournament_page_info)
        mock_create_tournament.assert_called_with(tournament_data)
     
      
    @patch.object(DBMS, 'write') 
    def test_assign_manual_score(self, mock_dbms_write):
        # Mocking necessary data
        score_info = {'sid':1}
        
        
        # call method
        self.educator.assign_manual_score(score_info)
        
        self.educator.DBMS.write.assert_called_with('ASSIGN_MANUAL_SCORE', score_info)
     
             
    def test_end_tournament(self):
        # Mocking necessary data
        someTournamentId = 1

        # Mocking the end_tournament method of the Tournament class
        with patch.object(Tournament, 'end_tournament') as mock_end_tournament:
            # call the method
            self.educator.end_tournament(someTournamentId)
        
        # Asserting that the expected methods were called
        mock_end_tournament.assert_called()
    
    def test_create_badge(self):
        # Mocking necessary data
        tournamentId = 1
        some_badge_logic = 'badge_logic'
        
        # Mocking the create_badge method of the Tournament class
        with patch.object(Tournament, 'create_badge') as mock_create_badge:
            # call the method
            self.educator.create_badge(tournamentId, some_badge_logic)
        
        # Asserting that the expected methods were called
        mock_create_badge.assert_called_with(some_badge_logic)
       
        
        
    def test_get_battle_page_info(self):
        # Mocking necessary data
        battleId = 1
        
        # Mocking the get_battle_page_info method of the Battle class
        with patch.object(Battle, 'get_battle_page_info') as mock_get_battle_page_info:
           # call the method
           self.educator.get_battle_page_info(battleId)
        
        # Mocking the get_unassigned_subscribers method of the Battle class
        with patch.object(Battle, 'get_unassigned_subscribers') as mock_get_unassigned_subscribers:
           # call the method
           self.educator.get_battle_page_info(battleId)
        
        # Asserting that the expected methods were called
        mock_get_battle_page_info.assert_called_with(self.uid)
        mock_get_unassigned_subscribers.assert_called()
        
        
    
    def test_get_tournament_page_info(self):
        # Mocking necessary data
        TournamentId = 1
        
        # Mocking the get_tournament_page_info method of the Tournament class
        with patch.object(Tournament, 'get_tournament_page_info') as mock_get_tournament_page_info:
           # call the method
           self.educator.get_tournament_page_info(TournamentId)
        
        # Asserting that the expected methods were called
        mock_get_tournament_page_info.assert_called()
        
    
    @patch.object(Educator, 'get_affiliation')
    def test_get_affiliation(self, mock_get_affiliation):
        # Set up mock response
        mock_get_affiliation.return_value = "some_affiliation"

        # Call the method
        result = self.educator.get_affiliation(self.uid)
        
        # Check if the method is called
        mock_get_affiliation.assert_called_once_with(self.uid)
        # Check if the result is as expected
        self.assertEqual(result, "some_affiliation")
    
        
    '''
    
    def test_get_tournaments
    
    def test_get_submission

    def test_score_submission
    
    def test_get_studentslist
    
    def test_get_submission_manuel_scoring
    
    
    
    
    def test_get_tournaments(self, mock_dbms_read):
        # Set up mock data for testing
        mockdf_tournaments = pd.DataFrame()
        
        mock_dbms_read.side_effect = [
            mockdf_tournaments,
        ]
        
        self.educator.get_tournaments()
        
        # Asserting that the expected methods were called
        self.assertIs(self.educator.get_tournaments, mockdf_tournaments)
        
    
    
    #def test_get_submission(self):
    
    
    def test_score_submission(self):
        # Mocking necessary data
        score = 1
        submissionId = 1
        
        self.educator.score_submission(score, submissionId)
        
        
        self.educator.DBMS.write.assert_called_with('ASSIGN_MANUAL_SCORE', {"_SCORE_": score,
                                                                            '_SUBMISSION_ID_':submissionId})
        
    
   
    def test_get_studentlist(self):
    
  
        
  
    def test_get_tournaments(self):
        # Set up mock data for testing
        mock_uid = 1
        mock_tournaments_data = [{'tournament_id': 1, 'tournament_name': 'Tournament 1'},
                                 {'tournament_id': 2, 'tournament_name': 'Tournament 2'}]

        # Set up Educator instance
        educator = Educator(mock_uid)
        educator.DBMS = self.mock_dbms

        # Mocking the DBMS read method
        self.mock_dbms.read.return_value = mock_tournaments_data

        # Call the method to test
        result = educator.get_tournaments()

        # Assert the results
        self.mock_dbms.read.assert_called_with("GET_EDUCATOR_TOURNAMENTS", mock_uid)
        self.assertEqual(result, mock_tournaments_data)

    def test_get_submission(self):
        # Set up mock data for testing
        mock_smid = 123
        mock_submission_data = {'submission_id': mock_smid, 'score': 95}

        # Set up Educator instance
        educator = Educator(1)
        educator.DBMS = self.mock_dbms

        # Mocking the DBMS read method
        self.mock_dbms.read.return_value = mock_submission_data

        # Call the method to test
        result = educator.get_submission(mock_smid)

        # Assert the results
        self.mock_dbms.read.assert_called_with('GET_SUBMISSIONS', {'_CONDITIONAL_': f"smid = {str(mock_smid)}"})
        self.assertEqual(result, mock_submission_data)

    def test_score_submission(self):
        # Set up mock data for testing
        mock_score = 90
        mock_smid = 456

        # Set up Educator instance
        educator = Educator(1)
        educator.DBMS = self.mock_dbms

        # Call the method to test
        educator.score_submission(mock_score, mock_smid)

        # Assert the results
        self.mock_dbms.write.assert_called_with('ASSIGN_MANUAL_SCORE', {'_SCORE_': mock_score, '_SUBMISSION_ID_': mock_smid})

    def test_get_studentslist(self):
        # Set up mock data for testing
        mock_students_data = {'user_name': ['Student1', 'Student2']}

        # Set up Educator instance
        educator = Educator(1)
        educator.DBMS = self.mock_dbms

        # Mocking the DBMS read method
        self.mock_dbms.read.return_value = mock_students_data

        # Call the method to test
        result = educator.get_studentslist()

        # Assert the results
        self.mock_dbms.read.assert_called_with("GET_STUDENTS", {})
        self.assertEqual(result, ('Student1', 'Student2', mock_students_data))
    
'''

if __name__ == '__main__':
    unittest.main()