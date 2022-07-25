from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "recipe_share"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name'] 
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# Create 

    @classmethod
    def create_user(cls,data):
        query = """INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(cls.db).query_db(query, data)
        
# Read

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query,data)
        users = []
        for user in results:
            users.append(cls(user))
        return users

# Validate 

    @staticmethod
    def validate_registration(user):
        is_valid = True
        user_in_db = User.get_by_email(user)
        if user_in_db:
            flash("Email is already in use", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("Letters only, Must be atleast 2 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Letters only, Must be atleast 2 characters.", "register")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be atleast 8 characters", "register")
            is_valid = False
        # checks if there is a digit in pw
        if not any(char.isdigit() for char in user['password']):
            flash('Password should have at least one number', "register")
            is_valid = False
        # checks if there is a CAP L in pw
        if not any(char.isupper() for char in user['password']):
            flash('Password should have at least one uppercase letter', "register")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords must match', "register")
        return is_valid


    # @staticmethod
    # def validate_login(user):
    #     is_valid = True 
    #     user_in_db = User.get_by_email(user)
    #     if user_in_db:
    #         flash("Email is already in use", "login")
    #         is_valid = False
    #     elif not bcrypt.check_password_hash(User(results[0]).password, user['password']):
    #         flash('Invalid email and password combination', 'login')
    #         is_valid = False
    #     if not EMAIL_REGEX.match(user['email']):
    #         flash('Invalid email address')
    #         is_valid = False
    #     return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True 
        user_in_db = User.get_by_email(user)
        if not user_in_db:
            flash("Email is not associated wih account", "login")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address', "login")
            is_valid = False
        if len(user['password']) <8 :
            flash("Password must be atleast 8 characters", "login")
            is_valid = False
        return is_valid




    # @staticmethod
    # def validate_registration(user):
    #     is_valid = True # we assume this is true
    #     user_in_db = User.get_by_email(user)
    #     if user_in_db:
    #         flash('Email already exists!')
    #         is_valid = False
    #     if len(user['first_name']) < 2:
    #         flash("Letters only, Must be atleast 2 characters.")
    #         is_valid = False
    #     if len(user['last_name']) < 2:
    #         flash("Letters only, Must be atleast 2 characters.")
    #         is_valid = False
    #     if not EMAIL_REGEX.match(user['email']):
    #         flash('Invalid email address')
    #     if len(user['password']) < 8:
    #         flash("Password must be atleast 8 characters")
    #         is_valid = False
    #     if not any(char.isdigit() for char in user['password']):
    #         flash('Password should have at least one number')
    #         is_valid = False
    #     if not any(char.isupper() for char in user['password']):
    #         flash('Password should have at least one uppercase letter')
    #         is_valid = False
    #     if user['password'] != user['confirm_password']:
    #         flash('Passwords must match')
    #     return is_valid


