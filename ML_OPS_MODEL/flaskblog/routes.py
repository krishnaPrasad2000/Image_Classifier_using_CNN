from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db,bcrypt
import secrets
import os
from PIL import Image
from flaskblog.forms import RegistrationForm, LoginForm,UploadImage
from flaskblog.models import User
from flask_login import login_user,login_required, current_user,logout_user
import cv2

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

value=''

@app.route("/home")
def home():
    
    return render_template('home.html')

@app.route("/")
@app.route('/start')
def start():
    return render_template('start.html',title='start')    


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data , email=form.email.data , password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully, now you can login with your credentials.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():

        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash( user.password , form.password.data):
             
             login_user(user , remember=form.remember.data)
             flash('You have logged in successfully','success')
             return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.', 'danger')      
        
    return render_template('login.html', title='Login', form=form)
     

def save_picture(form_picture):
     random_hex= secrets.token_hex(8)
     _, f_ext=os.path.splitext(form_picture.filename)
     picture_fn= random_hex + f_ext 
     picture_path=os.path.join(app.root_path,'static/profile_pics',picture_fn)
     form_picture.save(picture_path)
     
     output_size=(400,200)
    
     i=Image.open(form_picture)
     i.thumbnail(output_size)
     i.save(picture_path)
     return picture_fn

@app.route("/account",methods=['POST','GET'])
@login_required
def account():

    form=UploadImage()
    if form.validate_on_submit():
        if form.picture.data:
            form.picture.data
            picture_file=save_picture( form.picture.data)
            current_user.image_file=picture_file
            db.session.commit()
        return redirect(url_for('account'))

    user=User.query.filter_by(username=current_user.username).first()
    image_file=url_for('static',filename='profile_pics/'+ current_user.image_file)
    
    return render_template('account.html',title='Account',value=value,form=form,user=user,image_file=image_file)

@app.route("/predict",methods=['POST','GET'])
@login_required
def predict():

    user=User.query.filter_by(username=current_user.username).first()
    image_file=url_for('static',filename='profile_pics/'+ current_user.image_file)
    file_name="C:/Users/kp473/Documents/task3/flaskblog/"+image_file

    img_array= cv2.imread(file_name)
    img_array= cv2.cvtColor( img_array, cv2.COLOR_BGR2RGB)
    new_array= cv2.resize( img_array, (120,120))
    X_test=np.array( new_array, dtype=np.float32)

    model=tf.keras.models.load_model('final_model.h5')
    prediction=model.predict[X_test]
    categories =['iron_man','Hulk','captain_america','Thor']
    value=categories[np.argmax(prediction[0])]
    
    return render_template('ac_2.html',title='Account',value=value,user=user,image_file=image_file)

    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
