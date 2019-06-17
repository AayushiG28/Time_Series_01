import glob
import os
from flask import (make_response, Flask,session, g, json, Blueprint,flash, jsonify, redirect, render_template, request, url_for, send_from_directory)
import io

import csv
import pandas  as pd
from forms import RegistrationForm, LoginForm, LandingPage
import requests
import json
import pandas as pd
import numpy as np
encoding="utf-8"
lenght='0'

app = Flask(__name__)


app.config['SECRET_KEY'] = '26a8c98ee09f5655afde56fe90cebd76'

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")

@app.route("/")
def landingPage():
	session['loggedIn'] = False

	form = LandingPage()
	return render_template('landingpage.html',title='Welcome', form=form)

@app.route("/home")
def home():
	if(session['loggedIn']):

		return render_template('home.html')
	else:
		return render_template('logout.html')
	
@app.route('/results', methods=['GET', 'POST'])

def transform_view():
    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    data1 = pd.read_csv(stream,sep=';',index_col=0,parse_dates=True,decimal=',')
    num_timeseries = data1.shape[1]
    data_kw = data1.resample('2H').sum() / 8
    timeseries = []
    for i in range(num_timeseries):
        timeseries.append(np.trim_zeros(data_kw.iloc[:,i], trim='f'))
    
    prediction_times = [x.index[-1]+1 for x in timeseries[:1]]
    #print(prediction_times)
    data=series_to_obj(timeseries[1])
    api_url = "https://m5k2hqs5xj.execute-api.us-east-1.amazonaws.com/Final_DeepAr/deepar"
    body=json.dumps(data).encode(encoding)
    response_data = requests.post(url = api_url,data =body)
    #print(r)
    r=response_data.json()
    freq='H'
    prediction_length=10
    
    list_of_df = []
    for k in range(len(prediction_times)):
        prediction_index = pd.DatetimeIndex(start=prediction_times[k], freq=freq, periods=prediction_length)
        list_of_df.append(pd.DataFrame(data=r['predictions'][k]['quantiles'], index=prediction_index))

    return render_template('result.html', tables=[list_of_df[0].to_html(classes='data')], titles=list_of_df[0].columns.values)
    



@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form. username.data} , Please login!', 'success')
		session['email'] = request.form["email"]
		session['password'] = request.form["password"]
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	session['loggedIn'] = False
	if form.validate_on_submit():
		if form.email.data == 'admin@tata.com' and form.password.data == 'Tata@2019':
			session['loggedIn'] = True
			
			return redirect(url_for('home'))
		if 'email' and 'password' in session:
			if form.email.data == session['email'] and form.password.data == session['password']:
				session['loggedIn'] = True
				
				return redirect(url_for('home'))
			else:
				if(form.email.data == session['email']):
					flash(f'Login unsuccessful. Wrong combination of Email and password', 'danger')
				else:
					flash(f'User is not found. Please make sure you are registered with us', 'danger')
		else:
			flash(f'User is not found. Please make sure you are registered with us', 'danger')

	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	session['loggedIn'] = False

	return render_template('logout.html', title='Logout')

@app.route("/about")
def about():
	return render_template('about.html', title='About')
	
def series_to_obj(ts, cat=None):
    obj = {"start": str(ts.index[0]), "target": list(ts)}
    if cat is not None:
        obj["cat"] = cat
    return obj

if __name__ == '__main__':
	app.run(debug=True)