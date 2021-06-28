#Importing the Libraries
import numpy as np
from flask import Flask, request,render_template, session
from flask_cors import CORS
import os
import joblib
import pickle
import flask
import os
import newspaper
from newspaper import Article
import urllib
from fake_news_detection import news
from db_manager import *

#Loading Flask and assigning the model variable
app = Flask(__name__)
CORS(app)
app=flask.Flask(__name__,template_folder='templates')
app.secret_key='Sn0w_F14k3'

with open('model.pickle', 'rb') as handle:
	model = pickle.load(handle)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login',methods=['GET','POST'])
def login():
    	return render_template('login.html')
    		
@app.route('/logout',methods=['POST'])
def logout():
	if 'username' in session:
		session.pop('username',None)
		return render_template('login.html')
	else:
		return render_template('login.html',error = 'session not found')
        	  
@app.route('/admin',methods=['GET','POST'])
def admin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if dbcheckuserpass(username,password) == 'user exists':
			session['username']=request.form['username']
			return render_template('admin.html',name=request.form['username'])
		else:
			return render_template('login.html',error='incorrect username or password')
	else:
		return render_template('login.html',error='make sure you have logged in')

@app.route('/upload',methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		if 'username' in session:
			f = request.files['file']
			if '.csv' in f.filename:
				f.filename = 'uploaded.csv'
				f.save(f.filename)
				return render_template('admin.html',name=session['username'],msg='file has been uploaded sucessfully')
			else:
				return render_template('admin.html',name=session['username'],error='file not allowed')
		else:
			return render_template('login.html',error='session not found')
	else:
		return render_template('admin.html',name= session['username'],error='method not allowed')

@app.route('/update',methods=['POST'])
def update():
	if request.method == 'POST':
		if 'username' in session:
			if news() is True:
				return render_template('admin.html',name=session['username'],msg = 'dataset updated sucessfully')
			else:
				return render_template('admin.html',name=session['username'],error = 'error in updating the dataset')
		else:
			return render_template('login.html',error='session not found')	
	else:
		return render_template('admin.html',name=session['username'],error='method not allowed')

#Receiving the input url from the user and using Web Scrapping to extract the news content
@app.route('/predict',methods=['GET','POST'])
def predict():
    url =request.get_data(as_text=True)[5:]
    url = urllib.parse.unquote(url)
    article = Article(str(url))
    article.download()
    article.parse()
    article.nlp()
    news = article.summary
    print("\n",news,"\n")
    #Passing the news article to the model and returing whether it is Fake or Real
    pred = model.predict([news])
    return render_template('main.html', prediction_text='The news is "{}"'.format(pred[0]))
    
if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,debug=True,use_reloader=True)