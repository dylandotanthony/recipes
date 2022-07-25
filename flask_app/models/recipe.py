from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
import re

class Recipe:
    db = "recipe_share"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None




# Create
    @classmethod
    def create_recipe(cls,data):
        # if not cls.recipe_validation(data):
        #     return False
        query = """INSERT INTO recipes (name, description, instructions, under, date_cooked, user_id) 
        VALUES (%(name)s, %(description)s, %(instructions)s, %(under)s, %(date_cooked)s, %(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query,data)


# Read
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes =[]
        for row in results:
            recipe = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            recipe.user = User(user_data)
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        row = results[0]
        recipe = cls(row)
        return recipe

# Update
    @classmethod
    def update_recipe(cls,data,session_id):
        recipe = cls.get_by_id(data['id'])
        if recipe.user.id != session_id:
            flash("You must be the creator to update this recipe!")
            return False
        if not cls.validate_recipe(data):
            return False
        query = """UPDATE recipes
        SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s, under=%(under)s
        WHERE id =%(id)s;"""
        result = connectToMySQL(cls.db).query_db(query,data)
        recipe = cls.get_by_id(result["id"])
        return recipe

# delete 
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
        
    

# Validate      
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True 
        flash_message = "field is required and must be at least 3 characters"
        if len(recipe['name']) < 3:
            flash("Name " + flash_message, "recipe" )
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description " + flash_message, "recipe" )
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions " + flash_message, "recipe" )
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Date is required", "recipe")
            is_valid = False
        if "under" not in recipe:
            flash("Does the recipe take less that 30 minutes?", "recipe")
            is_valid = False
        return is_valid
