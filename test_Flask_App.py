'''This is a test suite for the what2Eat flask app. It is split
into two classes: integration and unit.
'''

import unittest
from unittest import mock, TestCase
from basic_Flask_app import *



class TestFlaskAppIntegration(unittest.TestCase):
    def setUp(self):
        app.testing = True 
        self.app = app.test_client()
       
    
    def test_home(self):
        '''Validates that the basic functionality of the homepage route works.
        it compares the expected string with the string generated by the
        function. As part of this test, it checks that it has the correct status
        code (200) -- necessary to fully validate its basic functionality.'''

        response = self.app.get('/', follow_redirects = True)
        expectedResult = "You have made it to the homepage for what2Eat, welcome :D.<br><br>" \
        "If you would like to return a list of products based on brand, please complete the URL with:<br>" \
        "/Products/brandName<br>Replace brandName with the brand you wish to query.<br><br>" \
        "Please note: Case matters, as does including spaces. If the brand is more than one word" \
        "replace the<br>spaces with %20 in the URL.<br> I.e., FRESH & EASY --> /Products/FRESH%20&%20EASY"
        self.assertEqual(expectedResult, response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def test_request_nonexistent_route(self):
        '''Tests the error handler for 404s. It prints a message to the web page
        that instructs the user on what the correct format of the URL.'''

        response = self.app.get('/68o5785vh/ghhjvhg/hjfvkf', follow_redirects = True)
        expectedResult = "Sorry, wrong format, do this: ...81/Products/brandName"
        self.assertEqual(expectedResult, response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)

    def test_route_to_get_All_Products(self):
        '''Tests that the route function that prints the products and related
        message to the web page.'''

        with mock.patch('what2Eat.ProductData.getAllProducts') as fake_data:
            fake_data.return_value = "abcdefg"
            response = self.app.get('/Products/FRESH & EASY', follow_redirects = True)
        outputString = "Here is the list of products for the brand FRESH & EASY <br>abcdefg"
        self.assertEqual(outputString, response.data.decode('utf-8'))


class TestFlaskAppUnit(unittest.TestCase):
    def setUp(self):
        app.testing = True 
        self.app = app.test_client()

    def test_get_All_Products(self):
        '''Tests the basic functionality of get_All_Products. It compares the
        expected string to the output string, they need to be equal to pass.'''

        with mock.patch('what2Eat.ProductData.getAllProducts') as fake_data:
            fake_data.return_value = "abcdefg"
            listOfBrandsStatement = get_all_products("Target")
        outputString = f"Here is the list of products for the brand Target <br>abcdefg"
        self.assertEqual(outputString, listOfBrandsStatement)

    def test_brand_Not_Found_Error(self):
        '''Test the error handling for the case when a user provides a brand that
        isn't in the dataset. It compares the expected string to the generateed
        string, must be equal to pass.'''

        with mock.patch('what2Eat.ProductData.returnBrands') as fake_data:
            fake_data.return_value = ['BrandA', 'BrandB', 'BrandC', 'BrandD']
            resultingString = brand_Not_Found_Error('BrandE')
        expectedString = f"The brand BrandE is not in the database.<br><br>" \
            f"The list of brands in the database are:<br>['BrandA', 'BrandB', 'BrandC', 'BrandD']."
        self.assertEqual(expectedString, resultingString)

if __name__ == '__main__':
    unittest.main()
