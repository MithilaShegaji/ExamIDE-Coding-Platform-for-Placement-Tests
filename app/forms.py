from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField, FieldList, FormField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from wtforms import Form  # <--- 1. IMPORT THE CORRECT BASE FORM CLASS
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TestForm(FlaskForm):
    name = StringField('Test Name', validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (in minutes)', validators=[DataRequired()])
    submit = SubmitField('Create Test')

class MCQOptionForm(Form): # Also a good practice to use Form here
    """Subform for a single MCQ option."""
    option_text = StringField('Option Text', validators=[DataRequired()])

class MCQQuestionForm(FlaskForm):
    """A form for creating/editing an MCQ question with dynamic options."""
    question_text = TextAreaField('Question Text', validators=[DataRequired()])
    marks = IntegerField('Marks', validators=[DataRequired()], default=1)
    options = FieldList(FormField(MCQOptionForm), min_entries=2, max_entries=10)
    correct_option = RadioField('Correct Option', choices=[], validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add MCQ Question')

# ==================================================================
# CORRECTED FORM DEFINITION
# ==================================================================
class TestCaseForm(Form):  # <--- 2. CHANGE FlaskForm TO Form
    """Subform for a single test case. Does not need CSRF."""
    input = TextAreaField('Input (stdin)', validators=[Optional()])
    expected_output = TextAreaField('Expected Output', validators=[DataRequired()])
# ==================================================================

class CodingQuestionForm(FlaskForm):
    """A form for creating/editing a coding question."""
    problem_statement = TextAreaField('Problem Statement', validators=[DataRequired()])
    marks = IntegerField('Marks', validators=[DataRequired()], default=10)
    difficulty = SelectField('Difficulty', 
                             choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], 
                             validators=[DataRequired()])
    
    starter_code_python = TextAreaField('Starter Code (Python)', validators=[Optional()])
    starter_code_java = TextAreaField('Starter Code (Java)', validators=[Optional()])
    starter_code_cpp = TextAreaField('Starter Code (C++)', validators=[Optional()])
    starter_code_c = TextAreaField('Starter Code (C)', validators=[Optional()])    
    starter_code_javascript = TextAreaField('Starter Code (starter_code_javascript)', validators=[Optional()])
    
    test_cases = FieldList(FormField(TestCaseForm), min_entries=2, max_entries=10)
    submit = SubmitField('Add Coding Question')