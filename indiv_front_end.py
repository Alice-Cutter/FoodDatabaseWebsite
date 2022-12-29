from flask import Flask, render_template, request
import csv

app = Flask(__name__)

data = []

@app.route('/')
def homepage():
    return render_template('index.html', rows=getRowTitles())

def load_data():
    with open('SampleData.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

def getRowTitles():
    row_titles = []
    for row in data:
        row_titles.append(row[0])

    return row_titles

def getRowByTitle(title):
     for row in data:
         if row[0] == title:
             return row
     return []

@app.route('/rowbytitle')
def display_row_by_title():
        value = getRowByTitle(request.args['rowchoice'])
        product = value[0]
        brand = value[1]
        ingredients = value[2].split(',')

        return render_template('productInfo.html', product=product, brand=brand, ingredients=ingredients)

@app.route('/aboutPage')
def display_about_page():
    return render_template('about.html')
@app.errorhandler(404)
def page_not_found(e):
     return render_template('404.html')

load_data()
app.run(host='0.0.0.0', port=81)

    