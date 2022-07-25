from flask import Flask, render_template, session, redirect, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash

# Read 
@app.route('/dashboard')
def dashboard():
    data ={
        'id': session["user_id"]
    }
    if "user_id" not in session:
        flash("You must be logged in to access dashboard!")
        return redirect('/')
    user = User.get_by_id(data)
    recipes = Recipe.get_all_recipes()
    return render_template('dashboard.html', user=user, recipes=recipes )

@app.route("/show/<int:recipe_id>")
def recipe_detail(recipe_id):
    data ={
        'id': session["user_id"]
    }
    recipe_data = {
        'id': recipe_id
    }
    user=User.get_by_id(data)
    recipe=Recipe.get_by_id(recipe_data)
    return render_template("show.html",user=user, recipe=recipe)

# Create 
@app.route("/create")
def create_recipe_page():
    data ={
        'id': session["user_id"]
    }
    user=User.get_by_id(data)
    return render_template("create.html", user=user)

@app.route("/recipe/create", methods=['POST'])
def create_recipe():
    valid_recipe = Recipe.validate_recipe(request.form)
    if not valid_recipe:
        return redirect(f'/create')
    Recipe.create_recipe(request.form)
    return redirect('/dashboard')

# Update 
@app.route("/edit/<int:recipe_id>")
def edit_page(recipe_id):
    data = {
        "id": recipe_id
    }
    recipe = Recipe.get_by_id(data)
    return render_template("update.html", recipe=recipe)

@app.route("/update/<int:recipe_id>", methods=['POST'])
def edit_recipe(recipe_id):
    valid_recipe = Recipe.validate_recipe(request.form) 
    if not valid_recipe:
        return redirect(f'/edit/{recipe_id}')
    return redirect('/dashboard')

# Delete 
@app.route("/delete/<int:recipe_id>")
def delete_by_id(recipe_id):
    data = {
        "id": recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")




