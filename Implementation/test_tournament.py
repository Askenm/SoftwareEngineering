import unittest
from unittest.mock import patch
from backend.backend import Educator, DBMS, Tournament, Battle
import pandas as pd


#self.educator.DBMS.write.assert_called_with('END_TOURNAMENT', {"_TOURNAMENT_ID_": tournament_id})


def test_create_battle(self):
        # Set up mock data for testing
        mock_uid = 1
        mock_tournament_id = 1
        mock_battle_data = {'_TOURNAMENT_ID_': mock_tournament_id}

        # Set up Educator instance
        educator = Educator(mock_uid)
        educator.DBMS = self.mock_dbms

        # Mocking the Tournament and Battle classes
        mock_tournament_instance = MagicMock()
        mock_tournament_instance.get_tournament_page_info.return_value = None
        mock_tournament_instance.create_battle.return_value = 123
        mock_battle_instance = MagicMock()
        self.mock_dbms.read.return_value = {'user_name': ['TestEducator']}
        educator.Tournament = MagicMock(return_value=mock_tournament_instance)
        educator.Battle = MagicMock(return_value=mock_battle_instance)

        # Call the method to test
        result = educator.create_battle(mock_battle_data)

        # Assert the results
        self.assertEqual(result, 0)
        mock_tournament_instance.get_tournament_page_info.assert_called_once()
        mock_tournament_instance.create_battle.assert_called_with(mock_battle_data)
        educator.Battle.assert_called_with(123)

def test_create_tournament(self):
        # Set up mock data for testing
        mock_uid = 1
        mock_tournament_data = {'tournament_name': 'New Tournament', 'start_date': '2024-02-01'}

        # Set up Educator instance
        educator = Educator(mock_uid)
        educator.DBMS = self.mock_dbms

        # Mocking the Tournament class
        mock_tournament_instance = MagicMock()
        mock_tournament_instance.get_tournament_page_info.return_value = {'tournament_id': 123}
        educator.Tournament = MagicMock(return_value=mock_tournament_instance)

        # Call the method to test
        result = educator.create_tournament(mock_tournament_data)

        # Assert the results
        self.assertEqual(result, {'tournament_id': 123})
        mock_tournament_instance.create_tournament.assert_called_with(mock_tournament_data)
    
def test_end_tournament(self):
        # Set up mock data for testing
        mock_tid = 1

        # Set up Educator instance
        educator = Educator(1)
        educator.Tournament = MagicMock()

        # Call the method to test
        educator.end_tournament(mock_tid)

        # Assert the results
        educator.Tournament.assert_called_with(mock_tid)
        educator.Tournament.return_value.end_tournament.assert_called_once()

def test_create_badge(self):
        # Set up mock data for testing
        mock_tid = 1
        mock_badge_logic = {'criteria': 'Some Criteria'}

        # Set up Educator instance
        educator = Educator(1)
        educator.Tournament = MagicMock()

        # Call the method to test
        result = educator.create_badge(mock_tid, mock_badge_logic)

        # Assert the results
        educator.Tournament.assert_called_with(mock_tid)
        educator.Tournament.return_value.create_badge.assert_called_with(mock_badge_logic)
        self.assertEqual(result, educator.Tournament.return_value.create_badge.return_value)


if __name__ == '__main__':
    unittest.main()