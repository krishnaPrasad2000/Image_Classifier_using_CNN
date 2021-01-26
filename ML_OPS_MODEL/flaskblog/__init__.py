from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
#app.config['SECRET_KEY'] = os.environ.get('SECRET')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)



from flaskblog import routes