import mysql.connector
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

def get_user_by_username(username):
    # Connect to your database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='adminpassword',
        database='faculty_hub'
    )

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user WHERE username = %s"
    cursor.execute(query, (username,))
    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if user_data:
        user = User(user_data['user_id'], user_data['username'], user_data['password'])
        return user

    return None
