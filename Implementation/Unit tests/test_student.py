import unittest
from unittest.mock import Mock, patch
from backend.backend import Student, DBMS, Tournament, Battle
#import psycopg2

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.uid = "some_user_id"
        self.student = Student(self.uid)

    def test_init(self):
        self.assertEqual(self.student.uid, self.uid)
        self.assertIsInstance(self.student.DBMS, DBMS)
        self.assertIsNone(self.student.tournament)
        self.assertIsNone(self.student.user_information)
        self.assertIsNone(self.student.battle)

    @patch.object(DBMS, 'read')
    def test_get_home_page(self, mock_dbms_read):
        # Set up mock responses
        mock_dbms_read.side_effect = [
            {"user_tournaments": [], "user_ongoing_tournaments": [], "user_upcoming_tournaments": []},
            {"user_battles": [], "user_ongoing_battles": [], "user_upcoming_battles": []},
            {"user_badges": []},
            {"user_name": "John Doe"}
        ]

        # Call the method
        self.student.get_home_page()

        # Check if the attributes are set correctly
        self.assertEqual(self.student.user_information["user_name"], "John Doe")

    @patch.object(DBMS, 'read')
    def test_get_battle_page_info(self, mock_dbms_read):
        # Set up mock responses
        mock_dbms_read.side_effect = [
            {"user_battles": [], "user_ongoing_battles": [], "user_upcoming_battles": []},
            {"user_badges": []},
            {"user_name": "John Doe"}
        ]

        # Mock Battle class
        with patch('your_module.Battle') as mock_battle:
            # Mock the battle instance
            mock_battle_instance = Mock()
            mock_battle.return_value = mock_battle_instance

            # Call the method
            self.student.get_battle_page_info("some_battle_id")

            # Check if the methods are called
            mock_battle_instance.get_battle_page_info.assert_called_once_with(self.uid)
            mock_battle_instance.get_unassigned_subscribers.assert_called_once()

    @patch.object(Tournament, 'get_tournament_page_info')
    def test_get_tournament_page_info(self, mock_tournament_page_info):
        # Call the method
        self.student.get_tournament_page_info("some_tournament_id")

        # Check if the method is called
        mock_tournament_page_info.assert_called_once()

    @patch.object(Tournament, 'get_affiliation')
    def test_get_affiliation(self, mock_get_affiliation):
        # Set up mock response
        mock_get_affiliation.return_value = "some_affiliation"

        # Call the method
        result = self.student.get_affiliation()

        # Check if the result is as expected
        self.assertEqual(result, "some_affiliation")

    @patch.object(Tournament, 'subscribe')
    def test_subscribe(self, mock_subscribe):
        # Call the method
        self.student.subscribe()

        # Check if the method is called
        mock_subscribe.assert_called_once_with(self.uid)

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
