import unittest
from unittest.mock import patch
from backend.backend import DBMS, Badge, datetime, Notification
import pandas as pd

class TestBadgeClass(unittest.TestCase):
    def setUp(self):
        
        self.tid = 1
        self.badge = Badge(self.tid)
    
    def test_init(self):
        self.assertEqual(self.badge.tid, self.tid)
        self.assertIsInstance(self.badge.DBMS, DBMS)
   
   
    @patch.object(DBMS, 'write')
    def test_create_badge_logic(self, mock_dbms_write):
        # Mocking necessary data
        mock_tid = 123  # Example tournament ID
        mock_badge_logic = {
            "criteria1": "value1",
            "criteria2": "value2"
            # Add more criteria as needed
        }

        self.badge.tid = mock_tid  # Set the tournament ID in the badge object

        # Call the method under test
        result = self.badge.create_badge_logic(mock_badge_logic)

        # Assert that the write method was called with the correct arguments
        expected_badge_logic = mock_badge_logic.copy()
        expected_badge_logic['_TOURNAMENT_ID_'] = mock_tid
        mock_dbms_write.assert_called_once_with("CREATE_BADGE", expected_badge_logic)

        # Assert the return value
        self.assertEqual(result, 0)
        

    @patch.object(DBMS, 'write')
    def test_assign_badge(self, mock_dbms_write):
        # Mocking necessary data
        mock_uid = 123  # Example user ID
        mock_bid = 456  # Example badge ID

        # Call the method under test
        self.badge.assign_badge(mock_uid, mock_bid)

        # Assert that the write method was called with the correct arguments
        mock_dbms_write.assert_called_once_with("AWARD_BADGE", {"_USER_ID_": mock_uid, "_BADGE_ID_": mock_bid})
 

    @patch('backend.backend.datetime')
    def test_get_current_date(self, mock_datetime):
        # Mock the current date
        mock_now = datetime(2024, 2, 6)  # Example current date
        mock_datetime.now.return_value = mock_now
        
        # Call the method under test
        current_date = self.badge.get_current_date()

        # Assert that datetime.now was called
        mock_datetime.now.assert_called_once()

        # Assert the return value
        expected_date = '2024-02-06'  # Expected formatted date
        self.assertEqual(current_date, expected_date)
    
    @patch.object(DBMS, 'read')
    @patch.object(Badge, 'get_current_date')
    def test_query_badge_notification_info(self, mock_get_current_date, mock_dbms_read):
        # Mocking necessary data
        mock_bid = 123  # Example badge ID
        mock_uid = 456  # Example user ID
        mock_badge_name = "Mock Badge Name"
        mock_tournament_name = "Mock Tournament Name"
        mock_tournament_id = 789
        mock_user_name = "Mock User Name"
        mock_current_date = "2024-02-06"  # Example current date

        # Create mock DataFrame for each read call
        mock_badge_name_df = pd.DataFrame({"badge_name": [mock_badge_name]})
        mock_tournament_df = pd.DataFrame({"tournament_name": [mock_tournament_name], "tid": [mock_tournament_id]})
        mock_user_name_df = pd.DataFrame({"user_name": [mock_user_name]})

        # Set up mock return values for mocked methods
        mock_dbms_read.side_effect = [mock_badge_name_df, mock_tournament_df, mock_user_name_df]
        mock_get_current_date.return_value = mock_current_date


        # Call the method under test
        notification_info = self.badge.query_badge_notification_info(mock_bid, mock_uid)

        # Assert that methods were called with the correct arguments
        mock_dbms_read.assert_any_call('GET_BADGE_NAME', {'_BADGE_ID_': mock_bid})
        mock_dbms_read.assert_any_call('GET_TOURNAMENT_NAME_FROM_BADGE_ID', {'_BADGE_ID_': mock_bid})
        mock_dbms_read.assert_any_call('GET_USER_NAME_FROM_UID', {'_USER_ID_': mock_uid})
        mock_get_current_date.assert_called_once()

        # Assert the returned notification_info dictionary
        expected_notification_info = {
            mock_uid: {
                "_BADGE_NAME_": mock_badge_name,
                "_USER_NAME_": mock_user_name,
                "_TOURNAMENT_NAME_": mock_tournament_name,
                "_TOURNAMENT_ID_": mock_tournament_id,
                "_BADGE_ACHIEVED_DATE_": mock_current_date
            }
        }
        self.assertEqual(notification_info, expected_notification_info)
    
    @patch.object(Badge, 'query_badge_notification_info')
    @patch.object(Notification, 'register_notfications_to_messageboard')
    @patch('backend.backend.Notification')
    def test_badge_awarded_notification(self, mock_notification, mock_register, mock_query):
        # Mocking necessary data
        mock_uid = 123  # Example user ID
        mock_bid = 456  # Example badge ID
        mock_notification_info = {"uid": mock_uid, "bid": mock_bid}  # Example notification info

        # Set up mock return value for mocked query_badge_notification_info method
        mock_query.return_value = mock_notification_info
        

        # Call the method under test
        self.badge.badge_awarded_notification(mock_uid, mock_bid)

        # Assert that query_badge_notification_info was called with the correct arguments
        mock_query.assert_called_once_with(mock_uid, mock_bid)

        # Assert that Notification constructor was called with the correct argument
        mock_notification.assert_called_once_with('BADGE_ACHIEVED')

       # Assert that register_notifications_to_messageboard was called with the correct argument
       # mock_register.assert_called_once_with(mock_notification_info)


    
    
    @patch.object(Badge, 'assign_badge')
    @patch.object(Badge, 'badge_awarded_notification')
    @patch.object(DBMS, 'read')
    def test_check_badge_achievers(self, mock_read, mock_notification, mock_assign_badge):
        # Mocking necessary data
        mock_bid = 123  # Example badge ID
        mock_logic_df = pd.DataFrame({
            "tournament_id": [456],  # Example tournament ID
            "rank": [3],  # Example rank
            "num_battles": [10]  # Example number of battles
        })
        mock_achievers_df = pd.DataFrame({"uid": [789, 1011]})  # Example potential badge achievers
        mock_existing_achievers_df = pd.DataFrame({"uid": [789]})  # Example current badge holders

        # Set up mock return values for mocked DBMS read method
        mock_read.side_effect = [
            mock_logic_df,
            mock_achievers_df,
            mock_existing_achievers_df,
            # Mock additional calls to DBMS.read, assuming they return an empty DataFrame
            pd.DataFrame(),  # Additional call 1
            pd.DataFrame()   # Additional call 2
            # Add more calls as needed
        ]

        # Call the method under test
        self.badge.check_badge_achievers(mock_bid)

        # Assert that read was called with the correct arguments
        mock_read.assert_any_call("GET_BADGE_LOGIC", {"_BADGE_ID_": mock_bid})
        mock_read.assert_any_call("GET_BADGE_ACHIEVERS", {
            "_TOURNAMENT_ID_": 456,  # Retrieved from mock_logic_df
            "_RANK_": 3,  # Retrieved from mock_logic_df
            "_NUM_BATTLES_": 10  # Retrieved from mock_logic_df
        })
        mock_read.assert_any_call("GET_CURRENT_BADGE_HOLDERS", {"_BADGE_ID_": mock_bid})

        # Assert that assign_badge and badge_awarded_notification were called with the correct arguments
        mock_assign_badge.assert_called_once_with(1011, mock_bid)  # Example new_awardee from mock_achievers_df
        mock_notification.assert_called_once_with(1011, mock_bid)  # Example new_awardee from mock_achievers_df

    


   
if __name__ == '__main__':
    unittest.main()
    
    
       
