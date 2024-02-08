import unittest
from unittest.mock import patch
from Implementation.backend.backend import Educator, DBMS, Tournament, Battle
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
    
    
    @patch('Implementation.backend.backend.Submission')
    @patch('Implementation.backend.backend.Notification')
    @patch('Implementation.backend.backend.DBMS.write')
    def test_assign_manual_score(self, mock_dbms_write, mock_notification, mock_submission):
        # Create an instance of Educator
        educator = Educator(uid=123)
        
        # Define mock data
        score_info = {'_SCORE_': 90, 'sid': 1}
        
        # Mock the methods of Submission and Notification
        mock_submission_instance = mock_submission.return_value
        mock_submission_instance.get_notification_info.return_value = {'notification_info': 'mock_data'}
        
        mock_notification_instance = mock_notification.return_value
        mock_notification_instance.register_notfications_to_messageboard.return_value = None
        
        # Call the method to be tested
        educator.assign_manual_score(score_info)
        
        # Assert that DBMS.write was called with the correct arguments
        mock_dbms_write.assert_called_once_with('ASSIGN_MANUAL_SCORE', score_info)
        
        # Assert that Submission and Notification instances were created and methods were called
        mock_submission.assert_called_once_with(1)
        mock_notification.assert_called_once_with('SUBMISSION_SCORED')
        mock_submission_instance.get_notification_info.assert_called_once()
        mock_notification_instance.register_notfications_to_messageboard.assert_called_once_with({'notification_info': 'mock_data'})
    

             
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
    
        
    
    
    @patch('Implementation.backend.backend.DBMS.read')
    def test_get_tournaments(self, mock_read):
        # Set up mock behavior for DBMS.read method
        mock_tournaments_data = [{'tournament_id': 1, 'tournament_name': 'Tournament 1'}, {'tournament_id': 2, 'tournament_name': 'Tournament 2'}]
        mock_read.return_value = mock_tournaments_data
        
        # Call the method to be tested
        tournaments = self.educator.get_tournaments()
        
        # Assert that DBMS.read was called with the correct arguments
        mock_read.assert_called_once_with("GET_EDUCATOR_TOURNAMENTS", 1)
        
        
     
    @patch('Implementation.backend.backend.DBMS.read')
    def test_get_submission(self, mock_read):
        # Set up mock behavior for DBMS.read method
        mock_submission_data = [{'smid': 1, 'submission_name': 'Submission 1'}, {'smid': 2, 'submission_name': 'Submission 2'}]
        mock_read.return_value = mock_submission_data
        
        # Call the method to be tested
        smid = 1
        submission = self.educator.get_submission(smid)
        
        # Assert that DBMS.read was called with the correct arguments
        mock_read.assert_called_once_with("GET_SUBMISSIONS", {'_CONDITIONAL_': f"smid = {str(smid)}"})
        
        # Assert the return value matches the expected value
        expected_submission = mock_submission_data
        self.assertEqual(submission, expected_submission)   
    
    #
    @patch('Implementation.backend.backend.DBMS.write')
    def test_score_submission(self, mock_write):
        # Set up mock behavior for DBMS.write method
        mock_write.return_value = None
        
        # Define test data
        score_info = {'_SCORE_': 85, '_SUBMISSION_ID_': 1}
        
        # Call the method to be tested
        self.educator.score_submission(score_info['_SCORE_'], score_info['_SUBMISSION_ID_'])
        
        # Assert that DBMS.write was called with the correct arguments
        mock_write.assert_called_once_with('ASSIGN_MANUAL_SCORE', score_info)
    
    
    @patch('Implementation.backend.backend.DBMS.read')
    def test_get_studentslist(self, mock_read):
        # Create an instance of Educator
        educator = Educator(uid=123)
        
        # Define mock data for DBMS.read method
        mock_data = pd.DataFrame({'user_name': ['Alice', 'Bob', 'Charlie']})
        mock_read.return_value = mock_data
        
        # Call the method to be tested
        students_list, _ = educator.get_studentslist()
        
        # Assert that DBMS.read was called with the correct arguments
        mock_read.assert_called_once_with("GET_STUDENTS", {})
        
        # Assert that the returned list of student names matches the mock data
        expected_students = ('Alice', 'Bob', 'Charlie')
        self.assertEqual(students_list, expected_students)
    
    
    @patch('Implementation.backend.backend.DBMS.read')
    def test_get_submission_manuel_scoring(self, mock_read):
        # Create an instance of Educator
        educator = Educator(uid=123)
        
        # Define mock data for DBMS.read method
        mock_data = pd.DataFrame({
            'smid': [1, 2, 3],
            'battle_id': [101, 102, 103],
            'group_name': ['Group A', 'Group B', 'Group C'],
            'submission_score': [80, 85, 90],
            'github_repo': ['repo1', 'repo2', 'repo3']
        })
        mock_read.return_value = mock_data
        
        # Call the method to be tested
        formatted_list, formatted_dict = educator.get_submission_manuel_scoring(uid=123)
        
        # Assert that DBMS.read was called with the correct arguments
        mock_read.assert_called_once_with("GET_SUBMISSION_FOR_SCORING", {"_EDUCATOR_ID_": 123})
        
        # Assert the formatted list of submissions
        expected_formatted_list = [
            "SMID:1 - battle_id: 101 - group_name: Group A - automatic score: 80",
            "SMID:2 - battle_id: 102 - group_name: Group B - automatic score: 85",
            "SMID:3 - battle_id: 103 - group_name: Group C - automatic score: 90"
        ]
        self.assertEqual(formatted_list, ["Select a submission"] + expected_formatted_list)
        
        # Assert the formatted dictionary of submissions
        expected_formatted_dict = {
            "SMID:1 - battle_id: 101 - group_name: Group A - automatic score: 80": [1, 'repo1'],
            "SMID:2 - battle_id: 102 - group_name: Group B - automatic score: 85": [2, 'repo2'],
            "SMID:3 - battle_id: 103 - group_name: Group C - automatic score: 90": [3, 'repo3']
        }
        self.assertEqual(formatted_dict, expected_formatted_dict)


if __name__ == '__main__':
    unittest.main()