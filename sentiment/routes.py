from flask import render_template, url_for, flash, redirect
from sentiment import app, api, db, bcrypt
from flask import request
import re
from textblob import TextBlob
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from sentiment.forms import RegistrationForm, LoginForm
from sentiment.models import User
from flask_login import login_user, current_user, logout_user, login_required
import datetime
import googleapiclient.discovery
from flask_mail import Mail, Message




@app.route('/')
@app.route('/chart', methods=['GET','POST'])
def chart():






    if request.method == 'POST':
        searchterm = request.form['text']
        today = datetime.date.today()

        yesterday = today - datetime.timedelta(days=1)

        db4= today - datetime.timedelta(days=2)


        labels = [db4 ,yesterday,today]

        tweets = api.search(q=searchterm, since=today, lang="en", count=100, tweet_mode='extended')

        tweets2 = api.search(q=searchterm, since=yesterday, until=today, lang="en", count=100, tweet_mode='extended')

        tweets3 = api.search(q=searchterm, since=db4, until=yesterday, lang="en", count=100, tweet_mode='extended')



        posts=[]
        posts2 = []
        posts3 = []
        postis = []
        def magic():

            for tweet in tweets:



                user_name = tweet.user.screen_name
                date = tweet.created_at

                if 'retweeted_status' in tweet._json:
                    tweet_text = tweet._json['retweeted_status']['full_text']
                else:
                    tweet_text = tweet.full_text

                def clean_tweet(tweeet):

                    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\ / \ / \S+)", " ", tweeet).split())

                def get_tweet_sentiment(tweeet):

                    blob = TextBlob(clean_tweet(tweeet))

                    if blob.sentiment.polarity > 0.0:
                        return 'positive'
                    elif blob.sentiment.polarity == 0.0:
                        return 'neutral'
                    else:
                        return 'negative'

                prop = get_tweet_sentiment(tweet_text)

                def create_list():
                    posts.append({'by': user_name, 'text': tweet_text, 'sentiment': prop, 'date': date})

                create_list()




        def magic2():

            for tweet in tweets2:



                user_name = tweet.user.screen_name
                date = tweet.created_at

                if 'retweeted_status' in tweet._json:
                    tweet_text = tweet._json['retweeted_status']['full_text']
                else:
                    tweet_text = tweet.full_text

                def clean_tweet(tweeet):

                    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\ / \ / \S+)", " ", tweeet).split())

                def get_tweet_sentiment(tweeet):

                    blob = TextBlob(clean_tweet(tweeet))

                    if blob.sentiment.polarity > 0.0:
                        return 'positive'
                    elif blob.sentiment.polarity == 0.0:
                        return 'neutral'
                    else:
                        return 'negative'

                prop = get_tweet_sentiment(tweet_text)

                def create_list():
                    posts2.append({'by': user_name, 'text': tweet_text, 'sentiment': prop, 'date': date})

                create_list()

        def magic3():

            for tweet in tweets3:

                user_name = tweet.user.screen_name
                date = tweet.created_at

                if 'retweeted_status' in tweet._json:
                    tweet_text = tweet._json['retweeted_status']['full_text']
                else:
                    tweet_text = tweet.full_text

                def clean_tweet(tweeet):

                    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) (\w+:\ / \ / \S+)", " ", tweeet).split())

                def get_tweet_sentiment(tweeet):

                    blob =TextBlob(clean_tweet(tweeet))

                    if blob.sentiment.polarity >= 0.5:
                        return 'positive'
                    elif -0.5 < blob.sentiment.polarity < 0.5 :
                        return 'neutral'
                    else:
                        return 'negative'

                prop = get_tweet_sentiment(tweet_text)

                def create_list():
                    posts3.append({'by': user_name, 'text': tweet_text, 'sentiment': prop, 'date': date})

                create_list()

        magic()
        ptweets = [post for post in posts if post['sentiment'] == 'positive']

        value1 = (100 * len(ptweets) / len(posts))
        ntweets= [post for post in posts if post['sentiment'] == 'negative']
        value2 = 100 * len(ntweets) / len(posts)

        newtweets = [post for post in posts if post['sentiment'] == 'neutral']
        value3 = 100 * len(newtweets) / len(posts)


        magic2()
        ptweets1 = [post for post in posts2 if post['sentiment'] == 'positive']

        value11 = (100 * len(ptweets1) / len(posts))
        ntweets1 = [post for post in posts2 if post['sentiment'] == 'negative']
        value21 = 100 * len(ntweets1) / len(posts)

        newtweets1 = [post for post in posts2 if post['sentiment'] == 'neutral']
        value31 = 100 * len(newtweets1) / len(posts)


        magic3()
        ptweets12 = [post for post in posts3 if post['sentiment'] == 'positive']

        value12 = (100 * len(ptweets12) / len(posts))
        ntweets2 = [post for post in posts3 if post['sentiment'] == 'negative']
        value22 = 100 * len(ntweets2) / len(posts)

        newtweets2 = [post for post in posts3 if post['sentiment'] == 'neutral']
        value32 = 100 * len(newtweets2) / len(posts)





        postis.extend(posts)
        postis.extend(posts2)
        postis.extend(posts3)

        posis = [value1, value11, value12]
        negis = [value2 ,value21, value22]
        newts = [value3 ,value31, value32]


        return render_template("Home.html", title='Home', vakues= posis, vakues1= negis, vakues2= newts, posts=postis, labels=labels,searchterm=searchterm)
    else:
        return render_template('Home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("chart"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data , email=form.email.data ,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(' your Account created  ', 'success')
        return redirect(url_for("login"))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = User.query.filter_by(email= form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash("You have been logged in!", 'success')
                return redirect(next_page) if next_page else redirect(url_for('chart'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("chart"))

@app.route("/account")
@login_required

def account():
    return render_template('account.html', title='Account')




mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'geargemun417@gmail.com'
app.config['MAIL_PASSWORD'] = '202259007ann417'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mailo = Mail(app)

@app.route("/mail",methods=['GET', 'POST'])

def mail():

    if request.method == 'POST':
        msg = Message(request.form['fname'], sender='sentiment417@gmail.com', recipients=['nkamau417@gmail.com'])
        msg.body = request.form['story']
        mailo.send(msg)
        flash('Email sent', 'success')

    return render_template('mail.html', title= 'mail')