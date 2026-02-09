import os
import pymysql
from urllib.request import urlopen

# os.getenv prevents passwords from being hard-coded in the source code, 
# they will not be committed to GitHub.
# Variables are declared outside the program, by the operating system or the shell.
db_config = {
    'host': os.getenv('DB_HOST', 'mydatabase.com'),
    'user': os.getenv('DB_USER', 'app_user'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'mydb')
}

def get_user_input():
    user_input = input('Enter your name: ')
    return user_input

def send_email(to, subject, body):
    os.system(f'echo {body} | mail -s "{subject}" {to}')

def get_data():
    # Changed HTTP to HTTPS for encrypted traffic
    # Changed to "secure-api"? Not sure if this was the issue
    url = 'https://secure-api.com/get-data'
    data = urlopen(url).read().decode()
    return data

def save_to_db(data):
    connection = None
    cursor = None
    # Added a try/finally block to ensure the cursor and database connection are always closed, 
    # even if an error occurs.
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        # Changed query to avoid building SQL with string formatting, 
        # helps to mitigate injection
        query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
        cursor.execute(query, (data, "Another Value"))
        connection.commit()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
