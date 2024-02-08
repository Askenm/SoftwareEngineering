import unittest
from unittest.mock import patch
from backend.backend import Authentication_info, DBMS, Badge, datetime, Notification
import pandas as pd

class TestAuthenticationInfoClass(unittest.TestCase):
    def setUp(self):
        
        self.auth_info = Authentication_info()
    
    def test_init(self):
        
        self.assertIsInstance(self.authen.DBMS, DBMS)
    
    @patch.object(DBMS, 'read')
    def test_get_credentials(self, mock_read):
        # Mocking necessary data
        mock_data = {
            'user_name': ['user1', 'user2'],
            'user_email': ['user1@example.com', 'user2@example.com'],
            'uid': [1, 2],
            'password': ['password1', 'password2'],
            'is_educator': [True, False]
        }

        # Convert mock data dictionary to DataFrame
        mock_df = pd.DataFrame(mock_data)

        # Set up mock return value for mocked DBMS read method
        mock_read.return_value = mock_df

        # Instantiate Authentication_info object
        auth_info = Authentication_info()

        # Call the method under test
        credentials = auth_info.get_credentials()

        # Define expected result
        expected_credentials = {
            'usernames': {
                'user1': {
                    'email': 'user1@example.com',
                    'id': 1,
                    'logged_in': False,
                    'name': 'user1',
                    'password': 'password1',
                    'role': 'Educator'
                },
                'user2': {
                    'email': 'user2@example.com',
                    'id': 2,
                    'logged_in': False,
                    'name': 'user2',
                    'password': 'password2',
                    'role': 'Student'
                }
            }
        }

        # Assert that the method returns the expected credentials
        self.assertEqual(credentials, expected_credentials)
    
    @patch.object(DBMS, 'read')
    def test_get_max_id(self, mock_read):
        # Mocking necessary data
        mock_max_id = 100  # Example max ID

        # Set up mock return value for mocked DBMS read method
        mock_read.return_value = pd.DataFrame({'max_id': [mock_max_id]})

        # Instantiate Authentication_info object
        auth_info = Authentication_info()

        # Call the method under test
        max_id = auth_info.get_max_id()

        # Assert that the method returns the expected max ID
        self.assertEqual(max_id, mock_max_id)


    @patch.object(DBMS, 'write')
    def test_add_user(self, mock_write):
        # Mocking necessary data
        mock_user_dict = {
            'email': 'user@example.com',
            'user_name': 'new_user',
            'password': 'new_password',
            'role': 'Student',
            'github': 'https://github.com/new_user'
        }

        # Instantiate Authentication_info object
        auth_info = Authentication_info()

        # Call the method under test
        auth_info.add_user(mock_user_dict)

        # Define expected call arguments for the mocked DBMS write method
        expected_call_args = {
            "_uid_": "DEFAULT",
            "_create_date_": "CURRENT_DATE",
            "_user_email_": 'user@example.com',
            "_user_name_": 'new_user',
            "_password_": 'new_password',
            "_is_educator_": False,
            "_github_": 'https://github.com/new_user'
        }

        # Assert that the method called DBMS write with the expected arguments
        mock_write.assert_called_once_with("ADD_USER", expected_call_args)
    
    @patch.object(DBMS, 'read')
    def test_get_uid_with_valid_username(self, mock_read):
        # Mocking necessary data
        mock_username = 'test_user'
        mock_uid = 123  # Example user ID

        # Set up mock return value for mocked DBMS read method
        mock_read.return_value = pd.DataFrame({'uid': [mock_uid]})

        # Instantiate Authentication_info object
        auth_info = Authentication_info()

        # Call the method under test
        uid = auth_info.get_uid(mock_username)

        # Assert that the method returns the expected user ID
        self.assertEqual(uid, mock_uid)

    @patch.object(DBMS, 'read')
    def test_get_uid_with_empty_username(self, mock_read):
        # Mocking necessary data
        mock_username = ''

        # Set up mock return value for mocked DBMS read method
        mock_read.return_value = pd.DataFrame()  # Empty DataFrame returned for empty username

        # Instantiate Authentication_info object
        auth_info = Authentication_info()

        # Call the method under test
        uid = auth_info.get_uid(mock_username)

        # Assert that the method returns an empty string for an empty username
        self.assertEqual(uid, '')

if __name__ == '__main__':
    unittest.main()