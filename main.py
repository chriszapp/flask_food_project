import pandas as pd
from flask import Flask, render_template, request
import random

# Initiate Flask App
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

# Initialize global variables
products = pd.read_csv('openfoodfacts_products.csv')

# Define functions
def filtering_df(strng, dframe):
    return dframe[dframe['id'] == strng]

## Make App working
@app.route("/")
def landing_page():
    return render_template('landing_page.html')

@app.route("/enter_login")
def enter_login():
  return render_template('login_page.html')

@app.route('/search', methods=['GET', 'POST'])
def enter_search():
  if request.method == 'POST':
    if int(request.form['s_code']) < 1000 and int(request.form['s_code']) >= 0:
      return render_template('search_brand.html', id_login = request.form['s_code'])
    else: 
      return render_template('wrong_page.html')

@app.route('/results', methods=['GET', 'POST'])
def search_page():
    print('HERE')
    if request.method == 'POST':
        id_input = request.form['brand']
        return render_template('result.html', obj = id_input, data = filtering_df(id_input, products))

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)