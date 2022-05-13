from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *
from wtforms.validators import *


class LoginForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired()])

    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=6, max=35)])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    email = EmailField('Email Address', [
        validators.DataRequired(),

    ])

    password = PasswordField('Create Password', [
        validators.DataRequired(),
        validators.length(min=6, max=35),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password")
    confirm = PasswordField('Repeat Password', description="Please retype your password to confirm it is correct")
    submit = SubmitField()

    def validate_password(self, password):
        errors = []
        lower_case_chars = "abcdefghijklmnopqrstuvwxyz"
        has_lower_case = False
        for char in self.password.data:
            if char in lower_case_chars:
                has_lower_case = True
        if not has_lower_case:
            errors.append('a lower case letter')

        upper_case_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        has_upper_case = False
        for char in self.password.data:
            if char in upper_case_chars:
                has_upper_case = True
        if not has_upper_case:
            errors.append(' an upper case letter')

        numbers = "0123456789"
        has_numbers = False
        for char in self.password.data:
            if char in numbers:
                has_numbers = True
        if not has_numbers:
            errors.append(' a number')

        if len(errors) != 0:
            error_string = f"Your password is missing the following characteristics: "
            for e in errors:
                error_string = error_string + e
            raise ValidationError(error_string)


class ProfileForm(FlaskForm):
    about = TextAreaField('About', [validators.length(min=6, max=300)],
                          description="Please add information about yourself")

    submit = SubmitField()


class UserEditForm(FlaskForm):
    about = TextAreaField('About', [validators.length(min=6, max=300)],
                          description="Please add information about yourself")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()

