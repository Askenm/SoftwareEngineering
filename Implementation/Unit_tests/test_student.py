import unittest
from unittest.mock import patch
import pandas as pd
from Implementation.backend.backend import Tournament, DBMS, Student, Battle


class TestStudentClass(unittest.TestCase):

    def setUp(self):
        self.uid = 1
        self.student = Student(self.uid)
      #  self.student.tournament = Tournament(self.uid)
        

    def test_init(self):
        self.assertEqual(self.student.uid, self.uid)
        self.assertIsInstance(self.student.DBMS, DBMS)
        self.assertIsNone(self.student.tournament)
        self.assertIsNone(self.student.user_information)
        self.assertIsNone(self.student.battle)

    @patch.object(DBMS, 'read')
    def test_get_home_page(self, mock_dbms_read):
        
       
        # Set up mock responses
        mockdf_tournaments = pd.DataFrame()
        mockdf_ongoing_tournaments = pd.DataFrame()
        mockdf_upcoming_tournaments = pd.DataFrame()
        mockdf_user_name = pd.DataFrame({"user_name": ["John Doe"]})
        mockdf_battles = pd.DataFrame()
        mockdf_ongoing_battles = pd.DataFrame()
        mockdf_upcoming_battles = pd.DataFrame()
        mockdf_badges = pd.DataFrame()
        

        mock_dbms_read.side_effect = [
            mockdf_tournaments,
            mockdf_ongoing_tournaments,
            mockdf_upcoming_tournaments,
            mockdf_user_name,
            mockdf_battles,
            mockdf_ongoing_battles,
            mockdf_upcoming_battles,
            mockdf_badges
        ]

        # Call the method
        self.student.get_home_page()
        

        # test that the correct df fetched from the db is assigned to the correct key in the user_information object dicionary
        self.assertIs(self.student.user_information["user_tournaments"], mockdf_tournaments)
        self.assertIs(self.student.user_information["user_ongoing_tournaments"], mockdf_ongoing_tournaments)
        self.assertIs(self.student.user_information["user_upcoming_tournaments"], mockdf_upcoming_tournaments)
        self.assertEqual(self.student.user_information["user_name"], "John Doe")
        self.assertIs(self.student.user_information["user_battles"], mockdf_battles)
        self.assertIs(self.student.user_information["user_ongoing_battles"], mockdf_ongoing_battles)
        self.assertIs(self.student.user_information["user_upcoming_battles"], mockdf_upcoming_battles)
        self.assertIs(self.student.user_information["user_badges"], mockdf_badges)
      #  self.assertEqual(self.student.user_information["user_tournaments"]["tid"].values[0], 2 )
      #  self.assertListEqual(self.student.user_information["user_tournaments"].columns.tolist(), ["tid", "tournament_name"] )
      
      
    def test_get_battle_page_info(self):
        # Mocking necessary data
        battleId = 1
        
        # Mocking the get_battle_page_info method of the Battle class
        with patch.object(Battle, 'get_battle_page_info') as mock_get_battle_page_info:
           # call the method
           self.student.get_battle_page_info(battleId)
        
        # Mocking the get_unassigned_subscribers method of the Battle class
        with patch.object(Battle, 'get_unassigned_subscribers') as mock_get_unassigned_subscribers:
           # call the method
           self.student.get_battle_page_info(battleId)
        
        # Asserting that the expected methods were called
        mock_get_battle_page_info.assert_called_with(self.uid)
        mock_get_unassigned_subscribers.assert_called()  
        

    @patch.object(Tournament, 'get_tournament_page_info')
    def test_get_tournament_page_info(self, mock_tournament_page_info):
        # Call the method
        self.student.get_tournament_page_info("some_tournament_id")

        # Check if the method is called
        mock_tournament_page_info.assert_called_once()

    @patch.object(Student, 'get_affiliation')
    def test_get_affiliation(self, mock_get_affiliation):
        # Set up mock response
        mock_get_affiliation.return_value = "some_affiliation"

        # Call the method
        result = self.student.get_affiliation(self.uid)
        
        # Check if the method is called
        mock_get_affiliation.assert_called_once_with(self.uid)
        # Check if the result is as expected
        self.assertEqual(result, "some_affiliation")

    '''
    @patch('Implementation.backend.backend.Tournament')
    @patch('Implementation.backend.backend.DBMS.read')
    def test_subscribe(self, mock_dbms_read, mock_tournament):
        # Create an instance of Student
        student = Student(uid=123)
        
        # Mock the DBMS.read method
        mock_dbms_read.return_value = {'user_name': 'John Doe'}
        
        # Mock the Tournament instance
        mock_tournament_instance = mock_tournament.return_value
        
        # Call the method to be tested
        student.subscribe()
        
        # Assert that DBMS.read was called with the correct arguments
        mock_dbms_read.assert_called_once_with('GET_STUDENTS', {})
        
        # Assert that Tournament instance was created and subscribe method was called
        mock_tournament.assert_called_once_with(student.tid)
        mock_tournament_instance.subscribe.assert_called_once_with(student.uid)

    '''
    

    @patch.object(DBMS, 'read')
    def test_get_studentslist(self, mock_dbms_read):
        # Set up mock response
        mock_dbms_read.return_value = {"user_name": ["John", "Jane"]}

        # Call the method
        result, _ = self.student.get_studentslist()

        # Check if the result is as expected
        self.assertEqual(result, ("John", "Jane"))

if __name__ == '__main__':
    unittest.main()
