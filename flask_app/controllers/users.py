import re
from flask import render_template,redirect,request,session,flash

from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template("index.html")


# Create 

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        # put the pw_hash into the data dictionary
        "password" : bcrypt.generate_password_hash(request.form['password'])
        }
    user = User.create_user(data)
    # store user id into session
    session['user_id'] = user
    flash('Registration Successful!', "register")
    return redirect('/dashboard')


@app.route("/login", methods=["POST"])
def login():
    if not User.validate_login(request.form):
        return redirect("/")
    user = User.get_by_email(request.form)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form["password"]):
            flash("Email/Password combination is incorrect")
            return redirect("/")
        session['user_id'] = user.id
        flash("Login was successful!")
        return redirect("/dashboard")
    flash("Email is not tied to an account")
    return redirect("/")
    #return user to form with validations



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')