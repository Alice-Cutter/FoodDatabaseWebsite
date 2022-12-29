import unittest
from webbrowser import get
from what2Eat import *
from unittest import TestCase, mock


class TestProductData(unittest.TestCase):
    def setUp(self):
        """Set the files used to test functions
        Written by Kana"""
        self.defaultSampleData = ProductData("SmallProductSheet.csv")
        self.emptySampleData = ProductData("emptyFileForTesting.csv")
        self.tenSampleData = ProductData("10LinesForTesting.csv")

    def test_load_csv_file(self):
        """Testing if the function load_csv_file returns a nested list
        Written by Kana"""
        result = self.defaultSampleData.load_csv_file()
        ifNested = any(isinstance(row, list) for row in result)
        self.assertTrue(ifNested)

    
    def test_returnBrands(self):
        """Testing the helper function returnBrands. The test function uses a small 
        sample of data to compare results
        Written by Morgan"""
        testBrandData = [("product_name","brand_name","ingredients"),
                        ('pizza', 'brand 1', 'flour, cheese'),
                        ('cereal', 'brand 2', 'oats, sugar, vitamin B'),
                        ('pot pie', 'brand 3', 'flour, beef, potato, onion')]
        with mock.patch('what2Eat.ProductData.load_csv_file') as mockLoad:
            mockLoad.return_value = testBrandData
            brands = ProductData('bogus.csv').returnBrands()
        accurateListOfBrands = ["brand 1","brand 2", "brand 3"]
        for brand in accurateListOfBrands:
            self.assertIn(brand, brands)
        self.assertNotIn("pot pie", brands)

    def test_returnBrandsOnlyBrands(self):
        """Testing that the helper function returnBrands only returns brands. 
        The test function uses a small sample of data to compare results.
        Written by Morgan"""        
        testBrandData = [("product_name","brand_name","ingredients"),
                        ('pizza', 'brand 1', 'flour, cheese'),
                        ('cereal', 'brand 2', 'oats, sugar, vitamin B'),
                        ('pot pie', 'brand 3', 'flour, beef, potato, onion')]
        with mock.patch('what2Eat.ProductData.load_csv_file') as mockLoad:
            mockLoad.return_value = testBrandData
            brands = ProductData('bogus.csv').returnBrands()
        self.assertNotIn('pizza', brands)
        self.assertNotIn('brand_name', brands) 

    def test_returnBrandsSingleInstanceOfBrands(self):
        """Testing that the helper function returnBrands only returns one instance of each brand. 
        The test function uses a small sample of data to compare results.
        Written by Morgan"""
        testBrandData = [('pizza', 'brand 1', 'flour, cheese'),
                        ('cereal', 'brand 2', 'oats, sugar, vitamin B'),
                        ('pot pie', 'brand 1', 'flour, beef, potato, onion')]
        with mock.patch('what2Eat.ProductData.load_csv_file') as mockLoad:
            mockLoad.return_value = testBrandData
            brands = ProductData('bogus.csv').returnBrands()
        self.assertEqual(1, brands.count('brand 1'))

    def test_returnBrandsNoEmptyStrings(self):
        """Testing that the helper function returnBrands does not return any empty strings. 
        The test function uses a small sample of data to compare results.
        Written by Morgan"""
        testBrandData = [('pizza', 'brand 1', 'flour, cheese'),
                        ('cereal', '', 'oats, sugar, vitamin B'),
                        ('pot pie', 'brand 3', 'flour, beef, potato, onion')]
        with mock.patch('what2Eat.ProductData.load_csv_file') as mockLoad:
            mockLoad.return_value = testBrandData
            brands = ProductData('bogus.csv').returnBrands()
        self.assertNotIn('', brands)
        self.assertEqual(2, len(brands))

    def test_returnBrandsEmptyList(self):
        """Testing that the helper function returnBrands returns an empty list if the passed
        list has no data beyond column lables. The test function uses a small sample of data 
        to compare results.
        Written by Morgan"""
        testBrandData = [("product_name","brand_name","ingredients")]
        with mock.patch('what2Eat.ProductData.load_csv_file') as mockLoad:
            mockLoad.return_value = testBrandData
            brands = ProductData('bogus.csv').returnBrands()   
        self.assertEqual([], brands)

    def test_returnBrandsEmptyFile(self):
        """Testing that the helper function returnBrands returns an empty list if the file is 
        totally empty. The test function uses a small sample of data to compare results.
        Written by Morgan"""
        testBrandData = []
        with mock.patch('what2Eat.ProductData.load_csv_file') as mockLoad:
            mockLoad.return_value = testBrandData
            brands = ProductData('bogus.csv').returnBrands()
        self.assertEqual([], brands)

    def test_returnBrandsFileNotFound(self):
        """Testing that the helper function returnBrands raises a FileNotFoundError if
        the file passed doesn't exist. 
        The test function uses a small sample of data to compare results.
        Written by Morgan"""
        with mock.patch("what2Eat.ProductData.load_csv_file") as mockLoad:
            mockLoad.side_effect = FileNotFoundError
            with self.assertRaises(FileNotFoundError):
                brands = ProductData('bogus.csv').returnBrands()

    def test_is_Valid_Brand_True(self):
        """Testing if the function is_Valid_Brand returns True when takeing in real brand
        Written by Alice."""
        validBrandBool = self.defaultSampleData.isValidBrand("G. T. Japan, Inc.")
        self.assertEqual(validBrandBool, True)

    def test_is_Valid_Brand_False(self):
        """Testing if the function is_Valid_Brand returns True when takeing in invalid brand
        Written by Alice."""
        invalidBrandBool = self.defaultSampleData.isValidBrand("G. T. China, Inc.")
        self.assertEqual(invalidBrandBool, False)

    def test_getIngredients(self):
        """Testing if the function getProductIngredients returns correct ingredients 
        Written by Isabella"""
        ingredients = self.defaultSampleData.getProductIngredients("Target Stores", "ROASTED RED PEPPER HUMMUS")
        testIngredients = "CHICKPEAS, ROASTED RED PEPPERS, SESAME TAHINI, CANOLA/OLIVE OIL BLEND, SALT, CITRIC ACID, NATURAL FLAVOR, GARLIC, SPICES, ACACIA GUM, XANTHAN GUM, GUAR GUM, POTASSIUM SORBATE AND SODIUM BENZOATE (TO MAINTAIN FRESHNESS).".lower()
        self.assertEqual(ingredients, testIngredients)

    def test_containsIngredient(self):
        """Testing if the function containsIngredient returns True when getting appropriate inputs 
        Written by Isabella"""
        result = self.defaultSampleData.containsIngredient("chickpeas", "Target Stores", "ROASTED RED PEPPER HUMMUS")
        self.assertTrue(result)
    
    def test_getProductIngredients(self):
        """Testing if getProductIngredients returns correct ingredients when getting correct product and brand names
        Written by Kana"""
        result =self.defaultSampleData.getProductIngredients("FRESH & EASY", "BARBECUE SAUCE")
        allIngredients = "tomato puree (water, tomato paste), sugar, distilled vinegar, molasses, water, modified corn starch, salt, bourbon whiskey, contains 1% or less of: mustard flour, spice, dried onion, dried garlic, natural flavor, xanthan gum, caramel color."
        self.assertEqual(result, allIngredients)

    def test_getIngredients_from_empty_file(self):
        """Testing if the function getProductIngredients returns None when attempting to retreive ingredients from an empty file 
        Written by Isabella"""
        ingredients = self.emptySampleData.getProductIngredients("brand", "product")
        self.assertEqual(ingredients, None)
    
    def test_getIngredients_invalid_brand(self):
        """Testing if the function getProductIngredients returns None when getting an invalid brand name
        Written by Isabella"""
        ingredients = self.defaultSampleData.getProductIngredients("family fare", "barbecue sauce")
        self.assertEqual(ingredients, None)

    def test_getProductIngredients_falseCombination(self):
        """Testing if getProductIngredients returns None when getting false combination of existing product and brand names
        Written by Kana"""
        result =self.defaultSampleData.getProductIngredients("Target Stores", "BARBECUE SAUCE")
        self.assertEqual(result, None)

    def test_isValidBrand_blank(self):
        """Testing if isValidBrand returns False when getting a blank as input
        Written by Kana"""
        result =self.defaultSampleData.isValidBrand("")
        self.assertFalse(result)

    def test_getAllProducts(self):
        """Testing if getAllProducts returns all products when getting a correct brand name
        Written by Kana"""
        result =self.defaultSampleData.getAllProducts("Stater Bros. Markets Inc.")
        allProducts = ['STATER BROS., SUGAR POWDERED','STATER BROS., PURE CANE SUGAR GRANULATED',
                       'STATER BROS., ROTINI AN ENRICHED MACARONI PRODUCT',
                       'STATER BROS., KIDNEY BEANS, DARK RED']
        self.assertEqual(result, allProducts)

    def test_containIngredients(self):
        """Testing if containIngredients returns True when getting appropriate input
        Written by Kana"""
        result =self.defaultSampleData.containsIngredient("molasses", "FRESH & EASY", "BARBECUE SAUCE")
        self.assertTrue(result)
    
    def test_containIngredients_FalseIngredients(self):
        """Testing if containIngredients returns alse when getting a wrong ingredient name
        Written by Kana"""
        result =self.defaultSampleData.containsIngredient("random product", "FRESH & EASY", "BARBECUE SAUCE")
        self.assertFalse(result)
    
    def test_containIngredients_FalseBrand(self):
        """Testing if containIngredients returns alse when getting a wrong brand name
        Written by Kana"""
        result =self.defaultSampleData.containsIngredient("molasses", "Random Brand", "BARBECUE SAUCE")
        self.assertFalse(result)
    
    def test_containIngredients_FalseProduct(self):
        """Testing if containIngredients returns alse when getting a wrong product name
        Written by Kana"""
        result =self.defaultSampleData.containsIngredient("molasses", "FRESH & EASY", "Random Product")
        self.assertFalse(result)

    def test_brandCarriesProduct_True(self):
        """Testing if brandCarriesProduct True when getting appropriate input
        Written by Kana"""
        result =self.defaultSampleData.brandCarriesProduct('FRESH & EASY', 'BARBECUE SAUCE')
        self.assertTrue(result)

    def test_brandCarriesProduct_FalseBrand(self):
        """Testing if brandCarriesProduct True when getting a wrong brand name
        Written by Kana"""
        result =self.defaultSampleData.brandCarriesProduct('Random Brand', 'BARBECUE SAUCE')
        self.assertFalse(result)
    
    def test_brandCarriesProduct_FalseProduct(self):
        """Testing if brandCarriesProduct True when getting a wrong product name
        Written by Kana"""
        result =self.defaultSampleData.brandCarriesProduct('FRESH & EASY', 'Random Product')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()

        
