from .. import util_classes
from .. import exceptions
import unittest
from unittest.mock import Mock, patch, MagicMock

class TestCampsitesManager(unittest.TestCase):
    def setUp(self):
        self.campsite_manager = util_classes.CampsitesManager()
        self.mock_app = Mock()
        self.mock_connection = Mock()
        self.mock_cursor = Mock()

        context_manager_mock = MagicMock()
        context_manager_mock.__enter__.return_value = (self.mock_connection, self.mock_cursor)
        self.mock_app.retrieve_db_connection.return_value = context_manager_mock
       
        
    def test_fetch_by_area_from_db(self):
        mock_rows = [{"site_ID": 1}, {"site_ID": 2}, {"site_ID": 3}]
        self.mock_cursor.fetchall.return_value = mock_rows
        
        result = self.campsite_manager.fetch_by_area(self.mock_app, "area1", 0, 3)
        
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(result, [1, 2, 3])
        
    def test_fetch_by_area_from_cache(self):
        self.campsite_manager.area_map["area1"] = [1, 2, 3, 4, 5]
        
        result = self.campsite_manager.fetch_by_area(self.mock_app, "area1", 1, 3)
    
        self.mock_cursor.execute.assert_not_called()
        self.assertEqual(result, [2, 3, 4])

    def test_fetch_by_area_add_to_cache(self):
        mock_rows = [{"site_ID": 4}, {"site_ID": 5}, {"site_ID": 6}]
        self.campsite_manager.area_map["area1"] = [1, 2, 3]

        self.mock_cursor.fetchall.return_value = mock_rows

        result = self.campsite_manager.fetch_by_area(self.mock_app, "area1", 3, 4)

        self.assertEqual(self.campsite_manager.area_map["area1"], [1, 2, 3, 4, 5, 6])
        self.assertEqual(result, [4, 5, 6])

    def test_fetch_by_overall_rating_from_db(self):
        mock_rows  = [{"site_ID": 1}]

        self.mock_cursor.fetchall.return_value = mock_rows

        result = self.campsite_manager.fetch_by_overall_rating(self.mock_app, 1)

        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(result, [1])

    def test_fetch_by_overall_rating_from_cache(self):
        self.campsite_manager.highest_rated_by_overall = [1, 2, 3, 4, 5]

        result = self.campsite_manager.fetch_by_overall_rating(self.mock_app, 3)
        
        self.mock_cursor.execute.assert_not_called()
        self.assertEqual(result, [1, 2, 3])
    
    def test_fetch_by_overall_rating_add_to_cache(self):
        mock_rows = [{"site_ID": 1}, {"site_ID": 2}, {"site_ID": 3}, {"site_ID": 4}, {"site_ID": 5}, {"site_ID": 6}]
        self.campsite_manager.highest_rated_by_overall = [1, 2, 3]

        self.mock_cursor.fetchall.return_value = mock_rows

        result = self.campsite_manager.fetch_by_overall_rating(self.mock_app, 6)

        self.assertEqual(self.campsite_manager.highest_rated_by_overall, [1, 2, 3, 4, 5, 6])
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_fetch_by_category_rating_from_db(self):
        mock_rows = [{"site_ID": 1}]

        self.mock_cursor.fetchall.return_value = mock_rows

        result = self.campsite_manager.fetch_by_category_rating(self.mock_app, "quietness", 1)

        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(result, [1])

    def test_fetch_by_category_rating_from_cache(self):
        self.campsite_manager.highest_rated_by_quietness = [1, 2, 3, 4, 5]
        result = self.campsite_manager.fetch_by_category_rating(self.mock_app, "quietness", 3)

        self.mock_cursor.execute.assert_not_called()
        self.assertEqual(result, [1, 2, 3])

    def test_fetch_by_category_rating_invalid_category(self):
        self.campsite_manager.highest_rated_by_category = {
            "category1": [1, 2, 3, 4, 5]
        }
        with self.assertRaises(ValueError):
            self.campsite_manager.fetch_by_category_rating(self.mock_app, "invalid_category", 3)

   








if __name__ == "__main__":
    unittest.main()