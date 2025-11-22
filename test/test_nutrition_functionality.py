import unittest
import os
import pandas as pd
import sys

# This block allows the test to find your 'nutrition.py' file
# by looking in the folder above the 'test' folder.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nutrition

class TestNutritionFunctionality(unittest.TestCase):

    def setUp(self):
        """
        Set up a temporary user for testing so we don't mess up real data.
        """
        self.test_user = "TestBot"
        self.test_file = os.path.join(nutrition.DATA_DIR, f"{self.test_user}_nutrition.csv")
        
        # Ensure we start with a clean slate (delete test file if it exists)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_1_calories_calculation(self):
        """
        Test if calorie math is correct.
        """
        # Create a fake mini-database for testing
        data = {'Food': ['TestApple'], 'Calories_per_100g': [50.0]}
        df = pd.DataFrame(data)
        
        # Test: 200g of an item with 50cal/100g should be 100 calories
        result = nutrition.calculate_calories('TestApple', 200, df)
        self.assertEqual(result, 100.0, "Calorie calculation logic is wrong.")
        print("\n✅ Test 1 Passed: Calorie calculation is accurate.")

    def test_2_save_functionality(self):
        """
        Test if data is actually saved to the CSV file.
        """
        success = nutrition.save_user_record(
            self.test_user, 
            "2025-01-01", 
            "TestApple", 
            200, 
            100.0
        )
        
        # Check 1: Did the function return True?
        self.assertTrue(success, "The save function returned False.")
        
        # Check 2: Does the file exist now?
        self.assertTrue(os.path.exists(self.test_file), "The CSV file was not created.")
        
        # Check 3: Is the data inside correct?
        df = pd.read_csv(self.test_file)
        self.assertEqual(len(df), 1, "There should be exactly 1 record in the file.")
        self.assertEqual(df['Food'][0], "TestApple", "The food name was saved incorrectly.")
        print("✅ Test 2 Passed: Data saving works correctly.")

    def tearDown(self):
        """
        Clean up: Delete the test CSV file after we are done.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    print("--- Starting Nutrition Module Tests ---")
    unittest.main(verbosity=2)