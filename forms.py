from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d')
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    type_id = SelectField('Project Type', coerce=int, validators=[DataRequired()])
    company_id = SelectField('Company', coerce=int, validators=[DataRequired()])
    school_id = SelectField('School', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Project')


class SchoolOfficeForm(FlaskForm):
    school_office = StringField('School/Office Name', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Add School/Office')



class ProjectTypeForm(FlaskForm):
    project_type = StringField('Project type', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Project Type')


class CompanyForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    discription = StringField('Discription', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    contact_number = StringField('Contact Details', validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Company')

