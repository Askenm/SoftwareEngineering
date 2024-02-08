import unittest
from unittest.mock import patch, call
from Implementation.backend.backend import Educator, DBMS, Tournament, Battle, Badge
import pandas as pd
import pandas.testing as pd_testing

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
        
    
    
    @patch('Implementation.backend.backend.DBMS.read')
    @patch('Implementation.backend.backend.DBMS.write')
    def test_create_battle(self, mock_write, mock_read):
        # Mock necessary data
        mock_battle_data = {
            '_BATTLE_NAME_': 'Example Battle Name',
            '_BATTLE_DESC_': 'Description of the Battle',
            '_TOURNAMENT_ID_': 123,
            '_BATTLE_REPO_': 'URL of the associated GitHub repository',
            '_BATTLE_CREATOR_': 'Creator ID',
            '_END_DATE_': 'End date of the battle',
            '_REGISTRATION_DEADLINE_': 'End date of registration for the battle',
            '_MIN_GROUP_SIZE_': 1,
            '_MAX_GROUP_SIZE_': 4,
            '_MANUAL_SCORING_': True
        }

        # Set up mock return value for DBMS.read to indicate battle name is available
        mock_read.return_value = pd.DataFrame({'count': [0]})

        # Set up mock return value for DBMS.write to indicate successful insertion
        mock_write.return_value.fetchone.return_value = (123,)  # Example battle ID

        # Call the method under test
        result = self.battle.create_battle(mock_battle_data)

        # Assert that the method returns 0 for successful creation
        self.assertEqual(result, 0)

        # Assert that DBMS.write was called with the correct parameters
        mock_write.assert_called_once_with("CREATE_BATTLE", mock_battle_data)
    
    
    
    @patch('Implementation.backend.backend.DBMS.read')
    def test_get_group_submissions(self, mock_read):
        # Mock necessary data
        mock_user_aff_educator = {
            'is_educator': True,
            'group_affiliation': pd.DataFrame()  # Empty DataFrame for educator
        }
        mock_user_aff_student = {
            'is_educator': False,
            'group_affiliation': pd.DataFrame({'gid': [456]})  # Example group ID for student
        }

        # Set up mock return value for DBMS.read for educator
        mock_read.return_value = pd.DataFrame({'submission_data': ['Educator Submission 1', 'Educator Submission 2']})

        # Call the method under test for educator
        submissions_educator = self.battle.get_group_submissions(mock_user_aff_educator)

        # Assert that DBMS.read was called with the correct parameters for educator
        mock_read.assert_called_once_with("GET_SUBMISSIONS", {"_CONDITIONAL_": "battle_id = 1"})

        # Assert that the returned submissions match the expected submissions for educator
        expected_submissions_educator = pd.DataFrame({'submission_data': ['Educator Submission 1', 'Educator Submission 2']})
        pd.testing.assert_frame_equal(submissions_educator, expected_submissions_educator)

        # Set up mock return value for DBMS.read for student
        mock_read.return_value = pd.DataFrame({'submission_data': ['Student Submission 1', 'Student Submission 2']})

        # Call the method under test for student
        submissions_student = self.battle.get_group_submissions(mock_user_aff_student)

        # Assert that DBMS.read was called with the correct parameters for student
        mock_read.assert_called_with("GET_SUBMISSIONS", {"_CONDITIONAL_": "battle_id = 1 AND g.gid = 456"})

        # Assert that the returned submissions match the expected submissions for student
        expected_submissions_student = pd.DataFrame({'submission_data': ['Student Submission 1', 'Student Submission 2']})
        pd.testing.assert_frame_equal(submissions_student, expected_submissions_student)
    
    
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
    
    
    @patch('Implementation.backend.backend.DBMS.read')
    def test_get_participants(self, mock_read):
        # Mock necessary data
        
        mock_participants_data = pd.DataFrame({'participant_id': [1, 2, 3], 'participant_name': ['User1', 'User2', 'User3']})

        # Set up mock return value for DBMS.read
        mock_read.return_value = mock_participants_data

        # Call the method under test
        participants = self.battle.get_participants()

        # Assert that DBMS.read was called with the correct parameters
        mock_read.assert_called_once_with('GET_PARTICIPANTS', {'_BATTLE_ID_': self.bid})

        # Assert that the number of participants matches the expected number
        expected_num_participants = len(mock_participants_data)
        self.assertEqual(len(participants), expected_num_participants)

        # Assert that each participant is as expected
        for i in range(expected_num_participants):
            expected_participant = mock_participants_data.iloc[i].values
            self.assertIn(expected_participant, participants)

    
    @patch('Implementation.backend.backend.Battle.get_user_affiliations')
    @patch('Implementation.backend.backend.DBMS')
    def test_get_battle_page_info(self, mock_dbms, mock_get_user_affiliations):
        # Mock necessary data
        mock_bid = 123  # Example battle ID
        mock_user_id = 456  # Example user ID
        mock_battle_data_df = pd.DataFrame({
            'battle_name': ['Example Battle'],
            'battle_description': ['Description of the Battle'],
            'github_repo': ['https://github.com/example_repo'],
            'tournament_id': [789]
        })
        
        mock_battle_rankings = pd.DataFrame({
        # Provide data that matches the expected shape of the DataFrame
            'rank 1': ['user1'],
            'rank 2': ['user2'],
        # Add columns as needed to match the shape of the DataFrame
        })
        
        mock_group_submissions = pd.DataFrame({
            'submission_id': [1, 2, 3],
            'user_id': [456, 789, 1011],
            'submission_score': [80, 90, 85]
        })
        mock_user_aff = {
            'is_educator': True,
            'group_affiliation': pd.DataFrame({'gid': []})
        }

        # Set up mock return value for get_user_affiliations
        mock_get_user_affiliations.return_value = mock_user_aff

        # Set up mock return value for DBMS.read
        mock_dbms_instance = mock_dbms.return_value
        mock_dbms_instance.read.side_effect = [
            mock_battle_data_df, 
            mock_battle_rankings]

        # Set up mock for get_group_submissions
        def mock_get_group_submissions(user_aff):
            return mock_group_submissions
        battle = Battle(bid=mock_bid)
        battle.get_group_submissions = mock_get_group_submissions

        # Set up mock for get_groups
        def mock_get_groups():
            pass
        battle.get_groups = mock_get_groups

        # Set up mock for get_participants
        mock_participants = pd.DataFrame({
            'user_id': [456, 789, 1011],
            'username': ['user1', 'user2', 'user3']
        })
        def mock_get_participants():
            return mock_participants
        battle.get_participants = mock_get_participants

        # Call the method under test
        battle.get_battle_page_info(uid=mock_user_id)

        # Assert that get_user_affiliations was called with the correct parameter
        mock_get_user_affiliations.assert_called_with(mock_user_id)

        # Assert that DBMS.read was called with the correct parameters
        mock_dbms_instance.read.assert_has_calls([
            call("GET_BATTLE_PAGE_INFO", {"_BATTLE_ID_": mock_bid}),
            call("GET_BATTLE_RANKINGS", {"_BATTLE_ID_": mock_bid})
        ])

        # Assert that get_group_submissions was called
        self.assertTrue(hasattr(battle, 'get_group_submissions'))

        # Assert that get_groups was called
        self.assertTrue(hasattr(battle, 'get_groups'))

        # Assert that get_participants was called
        self.assertTrue(hasattr(battle, 'get_participants'))

        # Assert that the battle data is set correctly
        self.assertEqual(battle.battle_data['battle_name'], 'Example Battle')
        self.assertEqual(battle.battle_data['battle_descriptions'], 'Description of the Battle')
        self.assertEqual(battle.battle_data['battle_repo'], 'https://github.com/example_repo')
        pd_testing.assert_frame_equal(battle.battle_data['submissions'], mock_group_submissions)
        pd_testing.assert_frame_equal(battle.battle_data['battle_rankings'], mock_battle_rankings)

    '''   
    @patch('backend.backend.Battle.get_battle_page_info')
    @patch('backend.backend.DBMS')
    @patch('backend.backend.Notification')
    def test_join_method(self, mock_notification_class, mock_dbms_class, mock_get_battle_page_info):
        # Mocking DBMS read and write methods
        mock_dbms_instance = mock_dbms_class.return_value
        mock_dbms_instance.read = lambda *args: {'user_name': 'mock_user_name', 'tournament_id': 'mock_tournament_id'}
        mock_dbms_instance.write = lambda *args, **kwargs: None

        # Mocking Notification register_notifications_to_messageboard method
        mock_notification_instance = mock_notification_class.return_value
        mock_notification_instance.register_notfications_to_messageboard = lambda *args: None

        # Creating a mock battle instance
        mock_bid = 123
        battle = Battle(bid=mock_bid)
        
        # Mocking user IDs and group name
        mock_user_ids = [101, 102, 103]
        mock_group_name = "Mock Group"

        # Mocking the get_battle_page_info method
        mock_get_battle_page_info.return_value = None

        # Calling the join method
        battle.join(mock_user_ids, mock_group_name)

        # Asserting DBMS write method was called with the correct parameters
        expected_group_info_calls = [((101,),), ((102,),), ((103,),)]
        mock_dbms_instance.write.assert_has_calls([call('JOIN_GROUP', {'_GROUP_NAME_': mock_group_name, '_BATTLE_ID_': mock_bid, '_USER_ID_': uid}) for uid in mock_user_ids])

        # Asserting Notification register_notfications_to_messageboard method was called with the correct parameters
        expected_notification_info = {
            101: {"_BATTLE_NAME_": battle.battle_data['battle_name'], '_USER_NAME_': 'mock_user_name', '_GROUP_NAME_': mock_group_name, '_TOURNAMENT_ID_': 'mock_tournament_id'},
            102: {"_BATTLE_NAME_": battle.battle_data['battle_name'], '_USER_NAME_': 'mock_user_name', '_GROUP_NAME_': mock_group_name, '_TOURNAMENT_ID_': 'mock_tournament_id'},
            103: {"_BATTLE_NAME_": battle.battle_data['battle_name'], '_USER_NAME_': 'mock_user_name', '_GROUP_NAME_': mock_group_name, '_TOURNAMENT_ID_': 'mock_tournament_id'}
        }
        mock_notification_instance.register_notfications_to_messageboard.assert_called_once_with(expected_notification_info)

    '''
        

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