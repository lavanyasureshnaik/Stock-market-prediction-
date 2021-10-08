
#import pymysql
from flask import Flask, render_template, url_for, flash, redirect, request , session
from forms import RegistrationForm, LoginForm
from get_tweets import TweetName
from front_end_gui import File_Pass
#import matplotlib.pyplot as plt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

#conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='xtipl')
#cur = conn.cursor()
#creating database
import sqlite3 
conn = sqlite3.connect('stock_database')
cur = conn.cursor()
try:
    cur.execute('''CREATE TABLE user (
    id integer Primary key  AUTOINCREMENT,
    name varchar(20),
    email varchar(50),
    password varchar(20))''')
    conn.commit()
except:
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#login_manager = LoginManager(app)
#login_manager.login_view = 'login'

@app.route('/')
#@app.route("/home")
def home():
    return render_template('home.html', title='home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/currentstock")
def stock():
    return render_template('stock.html', title='Current Stock')

@app.route("/register", methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('stock_database')
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['uname']
        email = request.form['email']
        password = request.form['psw']

        cur.execute("insert into user(name,email,password) values ('%s','%s','%s')" % (name, email, password))
        conn.commit()
        # cur.close()
        print('data inserted')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('stock_database')
    cur = conn.cursor()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        print('asd')
        count = cur.execute('SELECT * FROM user WHERE email = "%s" AND password = "%s"' % (email, password))
        print(count)
        # conn.commit()
        # cur.close()
        l = len(cur.fetchall())
        if l > 0:
            flash(f'Successfully Logged in')
            return render_template('account.html')
        else:
            print('hello')
            flash(f'Invalid Email and Password!')
    return render_template('login.html')

@app.route("/account")
#@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/onprediction", methods=['GET', 'POST'])
def onprediction():
    '''if request.method == 'GET':
        return render_template("onprediction.html")
    else:
        company = request.form['company']
        getweet = TweetName(company)
        print("deepak")
        getweet.get_tweets()'''
    return render_template('onprediction.html')


@app.route("/onsentiment", methods=['GET', 'POST'])
def onsentiment():

    return render_template('onsentiment.html',title='browse file')

@app.route("/price")
def price():
    return render_template('price.html')

@app.route("/onnifty50", methods=['GET', 'POST'])
def onnifty50():
    import csv

    with open('data.csv', newline='') as f:
        result = csv.reader(f)
        header = next(result)
        type(header)

        data = [row for row in result]

    return render_template('onnifty50.html', header=header, data=data)

@app.route("/prediction", methods=['GET', 'POST'])
def prediction():

        return render_template('prediction.html')

@app.route("/sentiment", methods=['GET', 'POST'])
def sentiment():
    if request.method == 'POST':
        company = request.form['company']
        getweet = TweetName(company)
        getweet.get_tweets()
    return render_template('sentiment.html')

@app.route('/analyse', methods=['POST', 'GET'])
def analyse():
    if request.method == 'POST':
        f = request.files['file']
        name = f.filename
        obj = File_Pass(name)
        data_out = obj.Analysiz_Text()
        labels = 'positive_sentiment', 'negative_sentiment', 'neutral_sentiment',
        sizes = [data_out[0], data_out[1], data_out[2]]
        explode = (0.1, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        fig1.savefig('static\my_plot.png')
        #plt.show()
        dict = {'Positive Sentiment': data_out[0], 'Negative Sentiment': data_out[1], 'Neutral Sentiment': data_out[2] }
        return render_template('display.html', result = dict)

@app.route("/logout")
def logout():
   session['logged_in'] = False
   return home()


if __name__ == '__main__':
    app.run(debug=True)
