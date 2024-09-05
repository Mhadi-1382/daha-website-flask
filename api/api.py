
'''
DAHA API . V1.0.0
=================

The API service is designed to access Daha platform information
so that developers can easily use different parts of the platform.

VIEW SOURCE CODE ON GITHUB: https://github.com/Mhadi-1382/daha-website-flask/
DOCS URL: https://dahauni.ir/api/
TERMS OF SERVICE: https://dahauni.ir/api/#terms/
'''

from flask import jsonify
import MySQLdb
import os

# Config DB
mysqlAPI = MySQLdb.connect(
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_NAME', 'DahaDB')
)

# Read user EMAILS from the database
user_auth_email_cursor = mysqlAPI.cursor()
user_auth_email_cursor.execute('SELECT emailApi FROM api')
# Read user PASSWORDS from the database
user_auth_password_cursor = mysqlAPI.cursor()
user_auth_password_cursor.execute('SELECT passwordApi FROM api')
# Convert database values to the dictionary for access easily values
user_auth = {
    "email": user_auth_email_cursor.fetchall(),
    "password": user_auth_password_cursor.fetchall()
}


class APIRunning:
    '''
    Call class and run the API rutes

    api_users() -- Receive all USERS from the database
    api_users_email()  -- Receive all EMAILS from the database
    api_ads()  -- Receive all ADS from the database
    '''
    def api_users():
        '''
        Receive all USERS from the database
        '''
        cursor_show_users_emails = mysqlAPI.cursor()
        cursor_show_users_emails.execute('SELECT * FROM users')
        return jsonify({"users": cursor_show_users_emails.fetchall()[2::]})
    def api_users_email():
        '''
        Receive all EMAILS from the database
        '''
        cursor_show_users_emails = mysqlAPI.cursor()
        cursor_show_users_emails.execute('SELECT email FROM users')
        return jsonify({"users_email": cursor_show_users_emails.fetchall()[2::]})
    def api_ads():
        '''
        Receive all ADS from the database
        '''
        cursor_show_users_ads = mysqlAPI.cursor()
        cursor_show_users_ads.execute('SELECT * FROM technologistset')
        return jsonify({"ads": cursor_show_users_ads.fetchall()})
