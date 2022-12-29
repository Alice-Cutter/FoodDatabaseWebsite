'''This is a program to run a basic app using Flask. It uses the funtions
written by the authors of What2Eat. It intends to demonstrate a simple
route based on the What2Eat code
'''

from flask import Flask
import csv
import what2Eat

app = Flask(__name__)

try: 
    what2EatObject = what2Eat.ProductData("SmallProductSheet.csv")
except:
    print("The dataset file was not found")

def get_all_products(brandName):
    '''Calls the getAllProducts method in what2Eat to return the products associated
    with the brand name it is passed. It prints a message to the screen that states
    the brand name entered and then lists the associated products'''
    listOfProducts = what2EatObject.getAllProducts(brandName)
    return f"Here is the list of products for the brand {brandName} <br>{listOfProducts}"

def brand_Not_Found_Error(brandName):
    '''Is called when the brand name that was passed is not included in the
    date set. It prints a message on the web page that tells the user as
    much and then provides a list with all of the brands in the dataset.'''
    allOfTheBrands = what2EatObject.returnBrands()
    return f"The brand {brandName} is not in the database.<br><br>" \
        f"The list of brands in the database are:<br>{allOfTheBrands}."

@app.route('/')
def homepage():
    '''The homepage for the app, provides user with brief instructions'''
    return "You have made it to the homepage for what2Eat, welcome :D.<br><br>" \
        "If you would like to return a list of products based on brand, please complete the URL with:<br>" \
        "/Products/brandName<br>Replace brandName with the brand you wish to query.<br><br>" \
        "Please note: Case matters, as does including spaces. If the brand is more than one word" \
        "replace the<br>spaces with %20 in the URL.<br> I.e., FRESH & EASY --> /Products/FRESH%20&%20EASY"

@app.route('/Products/<brandName>')
def request_for_products(brandName):
    '''Prints to the screen all of the products of the given brand'''
    if what2EatObject.isValidBrand(brandName):
        return get_all_products(brandName)
    return brand_Not_Found_Error(brandName)
    

@app.errorhandler(404)
def page_not_found(e):
    '''Error screen when the format of the URL is incorrect'''
    return "Sorry, wrong format, do this: ...81/Products/brandName"

@app.errorhandler(500)
def internal_server_error(e): 
    '''Error screen when an internal server error occures'''
    return "Hmmmm, that didn't seem to work. Use /81 to return to the homepage and /81/Products/brandName<br>" \
        "to query the products for the requested brand."

app.run(host='0.0.0.0', port=81)
