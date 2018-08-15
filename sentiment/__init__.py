from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


import tweepy


from tweepy import OAuthHandler


consumer_key = "Cifd3ZdKGKTZjL9WSS2dcPHjh"
consumer_secret = "r0EpCWOzPLbxNcSgX4OOKtuSPGvOjXYbq8JsacOGUHPLCYWHMZ"

access_token = "258672146-X8swzTiFO8mDHdPTDlL2pBmnBeV1yWW9Z9T5BBoo"
access_token_secret = "SkBganOTaKV1vU4yzLDwv8GBdv9tXaDGAmshWiHxRylNq"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

app = Flask(__name__)

app.config['SECRET_KEY'] = '2390cdb6e0d0d1ce9f2a2ab7da69d841'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view= 'login'
login_manager.login_message_category = 'info'


from  sentiment import  routes