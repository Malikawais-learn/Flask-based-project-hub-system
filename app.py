from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from flask_mysql_connector import MySQL
from flask_sqlalchemy import SQLAlchemy
from models import User, get_user_by_username
from forms import RegistrationForm, LoginForm, ProjectForm, SchoolOfficeForm, ProjectTypeForm, CompanyForm
from flask_login import LoginManager, logout_user, login_required, login_user, current_user


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Use your MySQL username
app.config['MYSQL_PASSWORD'] = 'adminpassword'
app.config['MYSQL_DB'] = 'faculty_hub'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

csrf = CSRFProtect(app)
mysql = MySQL(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:adminpassword@localhost/faculty_hub'
db = SQLAlchemy(app)



login_manager = LoginManager(app)



class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    discription = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    contact_email = db.Column(db.String(255), nullable=False)

    def __init__(self, company_name, discription, department, contact_number, contact_email):
        self.company_name = company_name
        self.discription = discription
        self.department = department
        self.contact_number = contact_number
        self.contact_email = contact_email










@login_manager.user_loader
def load_user(user_name):
    # Replace this with your actual user loading logic
    user_data = get_user_by_username(user_name)
    if user_data:
        user = User(user_data['user_id'], user_data['username'], user_data['password'])
        return user
    return None


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data and save user to the database
        username = form.username.data
        email = form.email.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO faculty_hub.user (username, password, email) VALUES (%s, %s, %s)',
                       (username, password, email))
        mysql.connection.commit()
        cursor.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)




@app.route('/', methods=['GET', 'POST'])
# @login_required
# def check_database_connection():
#     try:
#         cursor = mysql.connection.cursor()
#         cursor.execute('SELECT 1')
#         result = cursor.fetchone()
#         cursor.close()34
#
#         if result and result[0] == 1:
#             return 'Database is connected.'
#         else:
#             return 'Database is not connected.'
#
#     except Exception as e:
#         return 'Error connecting to database: {}'.format(str(e))

def home():
    return render_template('home.html')
    # if request.method == 'POST':
    #     note = request.form.get('note')#Gets the note from the HTML
    #
    #     if len(note) < 1:
    #         flash('Note is too short!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
    #         db.session.add(new_note) #adding the note to the database
    #         db.session.commit()
    #         flash('Note added!', category='success')

    # return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        print(user)
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username

            login_user(user, remember=True)
            flash('Logged in successfully.', 'success')
            return render_template('home.html')
            # return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html', form=form)


    # form = LoginForm()
    # if form.validate_on_submit():
    #     username = form.username.data
    #     password = form.password.data
    #
    #     cursor = mysql.connection.cursor(dictionary=True)
    #     query = 'SELECT * FROM faculty_hub.user WHERE username = %s AND password = %s'
    #     cursor.execute(query, (username, password))
    #     user = cursor.fetchone()
    #     cursor.close()
    #
    #     if user:
    #         # Set user data in the session for authentication
    #         session['user_id'] = user['user_id']
    #         flash('Login successful!', 'success')
    #         return redirect(url_for('dashboard'))
    #     else:
    #         flash('Login failed. Please check your credentials.', 'danger')
    #
    # return render_template('login.html', form=form)



    # form = LoginForm(request.form)
    # if request.method == 'POST' and form.validate():
    #     username = form.username.data
    #     password = form.password.data
    #
    #     # cursor = connection.cursor(dictionary=True)
    #     cursor = mysql.connection.cursor(dictionary=True)
    #     cursor.execute('SELECT * FROM faculty_hub.user WHERE username = %s', (username,))
    #     user_data = cursor.fetchone()
    #     cursor.close()
    #     print(user_data)
    #     print(user_data['password'])
    #     print(password)
    #     if user_data and user_data['password'] == password:
    #         session['user_id'] = user_data['id']
    #         session['username'] = user_data['username']
    #         flash('Logged in successfully.', 'success')
    #         return redirect(url_for('dashboard'))
    #     else:
    #         flash('Invalid username or password.', 'danger')
    #
    # return render_template('login.html', form=form)

@app.route('/logout')
# print('working before login required')
# @login_required
def logout():
    print('working after login required')
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))





@app.route('/add_school_office', methods=['GET', 'POST'])
# @login_required
def add_school_office():
    # if current_user.role != 'admin':
    #     flash('You do not have permission to access this page.', 'error')
    #     return redirect(url_for('dashboard'))

    form = SchoolOfficeForm()

    if form.validate_on_submit():
        school_office = form.school_office.data
        department = form.department.data

        # Create a MySQL cursor
        cursor = mysql.connection.cursor()

        # Insert data into the school_office table
        cursor.execute('INSERT INTO faculty_hub.school_office (school_office, Department) VALUES (%s, %s)',
                       (school_office, department))

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cursor.close()

        flash('School/Office added successfully.', 'success')
        return redirect(url_for('add_school_office'))

    return render_template('add_school_office.html', form=form)


@app.route('/add_project_type', methods=['GET', 'POST'])
# @login_required
def add_project_type():
    form = ProjectTypeForm()

    if form.validate_on_submit():
        project_type = form.project_type.data
        description = form.description.data

        # Create a MySQL cursor
        cursor = mysql.connection.cursor()

        # Insert data into the school_office table
        cursor.execute('INSERT INTO faculty_hub.project_type (project_type, Discription) VALUES (%s, %s)',
                       (project_type, description))

        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cursor.close()

        flash('Project Type added successfully.', 'success')
        return redirect(url_for('add_project_type'))

    return render_template('add_project_type.html', form=form)



@app.route('/add_company', methods=['GET', 'POST'])
# @login_required
def add_company():
    form = CompanyForm()

    if form.validate_on_submit():
        company_name = form.company_name.data
        discription = form.discription.data
        department = form.department.data
        contact_number = form.contact_number.data
        contact_email = form.contact_email.data

        # Create a MySQL cursor
        cursor = mysql.connection.cursor()

        # Insert data into the school_office table
        cursor.execute('INSERT INTO faculty_hub.company_list (company_name, discription, department, contact_number, contact_email) VALUES (%s, %s, %s, %s, %s)',
                       (company_name, discription, department, contact_number, contact_email))

         # Query all companies from the database
        # Commit the changes to the database
        mysql.connection.commit()

        # Close the cursor
        cursor.close()

        flash('Project Type added successfully.', 'success')
        return redirect(url_for('add_company'))

    # companies = Company.query.all()
    return render_template('add_company.html', form=form)

# @app.route('/add_project', methods=['GET', 'POST'])
# # @login_required
# def add_project():
#     form = ProjectForm()
#
#     # Populate select field choices
#     form.user_id.choices = [(user.id, user.username) for user in User.query.all()]
#     # form.type_id.choices = [(type.id, type.project_type) for type in ProjectType.query.all()]
#     # form.company_id.choices = [(company.id, company.company_name) for company in Company.query.all()]
#     # form.school_id.choices = [(school.school_id, school.school_office) for school in School.query.all()]
#
#     if form.validate_on_submit():
#         # Extract form data
#         project_name = form.project_name.data
#         description = form.description.data
#         start_date = form.start_date.data
#         end_date = form.end_date.data
#         user_id = form.user_id.data
#         type_id = form.type_id.data
#         company_id = form.company_id.data
#         school_id = form.school_id.data
#
#         # Create a MySQL cursor
#         cursor = mysql.connection.cursor()
#
#         # Insert data into the project table
#         cursor.execute(
#             'INSERT INTO faculty_hub.project (project_name, description, start_date, end_date, user_id, type_id, company_id, school_id) '
#             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
#             (project_name, description, start_date, end_date, user_id, type_id, company_id, school_id))
#
#         # Commit the changes to the database
#         mysql.connection.commit()
#
#         # Close the cursor
#         cursor.close()
#
#         flash('Project added successfully.', 'success')
#         return redirect(url_for('dashboard'))
#
#     return render_template('add_project.html', form=form)


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        username = session['username']
        print(user_id)
        print(username)


        if username == 'admin':
            # Admin-specific actions here
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            cursor.close()
            return render_template('admin_dashboard.html', username=username, users=users)
        else:
            # Fetch projects for internal user
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM faculty_hub.project WHERE user_id = %s', (user_id,))
            projects = cursor.fetchall()
            cursor.close()
            return render_template('internal_user_dashboard.html', username=username, projects=projects)

    else:
        flash('Please log in to access the dashboard.', 'info')
        return redirect(url_for('login'))

@app.route('/give_access/<int:user_id>')
def give_access(user_id):
    if 'user_id' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE users SET role = %s WHERE id = %s', ('internal', user_id))
        mysql.connection.commit()
        cursor.close()
        flash('Access granted to user ID {}'.format(user_id), 'success')
    else:
        flash('You are not authorized to perform this action.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/remove_project/<int:project_id>')
def remove_project(project_id):
    if 'user_id' in session and session['role'] == 'admin':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM projects WHERE id = %s', (project_id,))
        mysql.connection.commit()
        cursor.close()
        flash('Project ID {} has been removed.'.format(project_id), 'success')
    else:
        flash('You are not authorized to perform this action.', 'danger')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
