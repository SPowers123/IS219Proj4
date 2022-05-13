from flask import Blueprint, render_template, flash, url_for, abort
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from werkzeug.utils import redirect

from app.auth import admin_required
from app.db import db
from app.db.models import Recipe
from app.recipes.forms import RecipeAddForm

recipes = Blueprint('recipes', __name__, template_folder='templates')


@recipes.route('/recipes', methods=['GET'], defaults={"page": 1})
@recipes.route('/recipes/<int:page>', methods=['GET'])
@login_required
def browse_recipes(page):
    page = page
    per_page = 10
    pagination = Recipe.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    titles = [('title', 'Title'), ('user_id', 'Author ID')]
    retrieve_url = ('recipes.retrieve_recipe', [('recipe_id', ':id')])
    return render_template('browse_recipe.html', titles=titles, data=data, retrieve_url=retrieve_url, Recipe=Recipe)


@recipes.route('/recipes/view/<int:recipe_id>', methods=['GET'])
@login_required
def retrieve_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    return render_template('view_recipe.html', recipe=recipe)


@recipes.route('/recipes/add', methods=['POST', 'GET'])
@login_required
def add_recipe():
    addrecipeform = RecipeAddForm()
    if addrecipeform.validate_on_submit():
        recipe = Recipe(title=addrecipeform.recipe_title.data, content=addrecipeform.recipe_content.data,
                        user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash("Added a new recipe!", "success")
        return redirect(url_for('recipes.my_recipes'))
    try:
        return render_template('add_recipe.html', form=addrecipeform)
    except TemplateNotFound:
        abort(404)


@recipes.route('/recipes/edit/<int:recipe_id>', methods=['POST', 'GET'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if current_user.id != recipe.user_id and current_user.is_admin is False:
        flash("You cannot edit this recipe")
        return redirect(url_for('recipes.my_recipes'))

    editrecipeform = RecipeAddForm(obj=recipe)
    if editrecipeform.validate_on_submit():
        db.session.delete(recipe)
        recipe = Recipe(title=editrecipeform.recipe_title.data, content=editrecipeform.recipe_content.data,
                        user_id=current_user.id)
        db.session.add(recipe)
        db.session.commit()
        flash("Edited a recipe!", "success")
        return redirect(url_for('recipes.my_recipes'))
    return render_template('add_recipe.html', form=editrecipeform)


@recipes.route('/recipes/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if current_user.id == recipe.user_id or current_user.is_admin:
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted', 'success')
    else:
        flash("You may not delete this recipe")
    return redirect(url_for('recipes.my_recipes'))


@recipes.route('/recipes/mine', methods=['GET'], defaults={"page": 1})
@recipes.route('/recipes/mine/<int:page>', methods=['GET'])
@login_required
def my_recipes(page):
    page = page
    per_page = 10
    pagination = Recipe.query.filter(Recipe.user_id == current_user.id).paginate(page, per_page, error_out=False)
    data = pagination.items
    titles = [('title', 'Title'), ('user_id', 'Author ID')]
    retrieve_url = ('recipes.retrieve_recipe', [('recipe_id', ':id')])
    edit_url = ('recipes.edit_recipe', [('recipe_id', ':id')])
    add_url = url_for('recipes.add_recipe')
    delete_url = ('recipes.delete_recipe', [('recipe_id', ':id')])
    return render_template('browse_recipe.html', titles=titles, data=data, add_url=add_url, edit_url=edit_url,
                           delete_url=delete_url, retrieve_url=retrieve_url, Recipe=Recipe)


@recipes.route('/recipes/admin', methods=['GET'], defaults={"page":1})
@recipes.route('/recipes/admin/<int:page>', methods=['GET'])
@login_required
@admin_required
def manage_recipes(page):
    page = page
    per_page = 10
    pagination = Recipe.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    titles = [('title', 'Title'), ('user_id', 'Author ID')]
    retrieve_url = ('recipes.retrieve_recipe', [('recipe_id', ':id')])
    edit_url = ('recipes.edit_recipe', [('recipe_id', ':id')])
    add_url = url_for('recipes.add_recipe')
    delete_url = ('recipes.delete_recipe', [('recipe_id', ':id')])
    return render_template('browse_recipe.html', titles=titles, data=data, add_url=add_url, edit_url=edit_url,
                           delete_url=delete_url, retrieve_url=retrieve_url, Recipe=Recipe)