from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class RecipeAddForm(FlaskForm):
    recipe_title = StringField('Title', [validators.DataRequired()], description="Title your recipe")
    recipe_content = TextAreaField('Recipe', [validators.DataRequired()], description="Write your recipe here")
    submit = SubmitField()