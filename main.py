import pandas as pd
from flask import Flask, render_template, request
import random

# Initiate Flask App
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

students = pd.read_csv('StudentsPerformance.csv')

math_mean = round(students['math score'].mean())
read_mean = round(students['reading score'].mean())
write_mean = round(students['writing score'].mean())

def check_positioning (student_score, subject):
  return 'Congratulation, you are among the best 10% of the school!!' if student_score >= students[subject + ' score'].quantile(0.9) else \
  'Congratulation, you are among the best 25% of the school!' if student_score >= students[subject + ' score'].quantile(0.75) else\
   "It's a good result, but keep improving!" if student_score >= 60 else\
   'Not yet, keep working!'

## Make App working
@app.route("/")
def landing_page():
    return render_template('landing_page.html')

@app.route("/enter_login")
def enter_login():
  # print("in enter_login")
  return render_template('login_page.html')

@app.route('/', methods=['GET', 'POST'])
def login_page():
  print('in login')
  student_data = {}
  if request.method == 'POST':

    if int(request.form['s_code']) < 1000 and int(request.form['s_code']) >= 0:
      
      student_number = int(request.form['s_code'])

      math_score = students.iloc[student_number]['math score']
      read_score = students.iloc[student_number]['reading score']
      write_score = students.iloc[student_number]['writing score']

      # Fill the data dictionary
      student_data['number'] = 'MS01' + str(student_number).zfill(4)
      student_data['math_score'] = math_score
      student_data['read_score'] = read_score
      student_data['write_score'] = write_score
      student_data['math_mean'] = math_mean
      student_data['read_mean'] = read_mean
      student_data['write_mean'] = write_mean
      student_data['math_comment'] = check_positioning (math_score, 'math')
      student_data['read_comment'] = check_positioning (read_score, 'reading')
      student_data['write_comment'] = check_positioning(write_score, 'writing')

    else: 
      return render_template('wrong_student.html')

    # Send data to the next page
    return render_template('result_page.html', student_data = student_data)

if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)