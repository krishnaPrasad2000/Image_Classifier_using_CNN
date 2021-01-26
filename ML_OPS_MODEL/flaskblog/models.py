from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    image_file=db.Column(db.String(20),nullable=False,default='464c2fb5c5aa406c.jpg')
    username = db.Column(db.String(20), unique=True, nullable=False )
    email = db.Column(db.String(130), unique=True , nullable= False)
    password= db.Column(db.String(130),unique=False , nullable= False) # password_hash ##study it
   
    

