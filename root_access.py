
'''
DAHA CLI: ROOT ACCESS DATABASE . VER 1.0.0
GITHUB: https://github.com/Mhadi-1382/daha-website-flask
'''

from app import username_admin, email_admin
from colorama import Fore
from time import sleep
import MySQLdb
import sys
import os

try:
    mysqlCLI = MySQLdb.connect(
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_USER', 'root'),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_NAME', 'DahaDB'),
        # int(os.getenv('DB_PORT', 55063))
    )
    print("DATABASE CONECTED.")
except:
    print("DATABASE NOT CONECT.")
    exit()

# PASSWORD & DATE ADMIN
password_admin = "root"
date_admin = "R"

def login_root_access():
    '''LOGIN ROOT ACCESS'''
    # CREATE ROOT USER IF NOT EXISTS
    try:
        cursorCLI = mysqlCLI.cursor()
        if cursorCLI.execute("SELECT * FROM users WHERE userName = 'root'"):
            pass
        else:
            cursorCLI = mysqlCLI.cursor()
            cursorCLI.execute("INSERT INTO users (userName, email, password, dateSingin) VALUES (%s,%s,%s,%s)", (f'root', '', f'{email_admin}', f'{date_admin}',))
            mysqlCLI.commit() 
    except:
        print(0)

    print()
    queryUsernameCLI = str(input('⊢ USERNAME ... '))
    queryPasswordCLI = str(input('⊢ PASSWORD ... '))

    cursorCLI = mysqlCLI.cursor()
    if cursorCLI.execute("SELECT * FROM users WHERE userName = %s AND password = %s", (queryUsernameCLI, queryPasswordCLI,)) and ("root", f"{username_admin}"):
        print(Fore.LIGHTGREEN_EX + "[✔] ACCESS IS ALLOWED." + Fore.WHITE)
    else:
        print(Fore.YELLOW + "[!] NOT FOUND USER/NOT HAVING ACCESS." + Fore.WHITE)
        login_root_access()
        
login_root_access()

sleep(3)
if sys.platform != "win32":
    os.system("CLEAR")
else:
    os.system("CLS")

splashCLI = '''DAHA CLI
ROOT ACCESS.

[0] Create Admin User
[1] Show Details User
[2] Delete User
[3] Exit CLI
'''
print(splashCLI)

def create_admin_user():
    '''CREATE ADMIN USER'''
    cursorCLI = mysqlCLI.cursor()
    cursorCLI.execute("INSERT INTO users (userName, email, password, dateSingin) VALUES (%s,%s,%s,%s)", (f'{username_admin}', f'{email_admin}', f'{password_admin}', f'{date_admin}',))
    mysqlCLI.commit()

    print(f"USERNAME: {username_admin}")
    sleep(1)
    print(f"EMAIL: {email_admin}")
    sleep(1)
    print(f"PASSWORD: {password_admin}")
    print()
    sleep(1)

    print(Fore.LIGHTGREEN_EX + "[✔] CREATE ADMIN USER." + Fore.WHITE + "\n")

def show_details_user():
    '''SHOW DETAILS USER'''
    cursorCLI = mysqlCLI.cursor()
    cursorCLI.execute("SELECT * FROM users")
    print()
    for u in cursorCLI.fetchall():
        print(u)
    print()

def delete_user():
    '''DELETE USER'''
    inputIDUser = int(input('⊢ USER ID ... '))
    cursorCLI = mysqlCLI.cursor()

    if cursorCLI.execute(f"SELECT * FROM users WHERE id = {inputIDUser}"):
        cursorCLI.execute(f"DELETE FROM users WHERE id = {inputIDUser}")
        mysqlCLI.commit()

        print(Fore.LIGHTGREEN_EX + f"[✔] THE USER WAS REMOVED WITH ID {inputIDUser}." + Fore.WHITE + "\n")
    else:
        print(Fore.YELLOW + "[!] ID DO NOT EXIST." + Fore.WHITE + "\n")

while True:
    query = input('Please Select The Option: ')

    if int(query) == 0:
        create_admin_user()
    elif int(query) == 1:
        show_details_user()
    elif int(query) == 2:
        delete_user()
    elif int(query) == 3:
        mysqlCLI.close()
        break
    else:
        print(Fore.YELLOW + "[!] INVALID COMMAND." + Fore.WHITE)
