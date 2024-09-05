
'''
DAHA CLI: ROOT ACCESS DATABASE . V1.1.0
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
        os.getenv('DB_NAME', 'DahaDB')
    )
    print("DATABASE CONECTED.")
except:
    print("DATABASE NOT CONECT.")
    exit()

# PASSWORD & DATE ADMIN
password_admin = ""
date_admin = ""

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
[1] Show Details Users
[2] Show Details Teachers
[3] Delete User & Teacher
[4] Exit CLI
'''
for i in splashCLI:
    print(f"{i}", end="", flush=True)
    sleep(0.05)
print()

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

def show_details_users():
    '''SHOW DETAILS USERS'''
    cursorCLI = mysqlCLI.cursor()
    cursorCLI.execute("SELECT * FROM users")
    print()
    for u in cursorCLI.fetchall():
        print(u)
    print()

def show_details_teachers():
    '''SHOW DETAILS TEACHERS'''
    cursorCLI = mysqlCLI.cursor()
    cursorCLI.execute("SELECT * FROM teachers")
    print()
    for u in cursorCLI.fetchall():
        print(u)
    print()

def delete_user_teacher():
    '''DELETE USER & TEACHER'''
    inputQuerySelectUser = input('⊢ USER/U or TEACHER/T: ')
    
    if inputQuerySelectUser  == "USER" or inputQuerySelectUser  == "user" or inputQuerySelectUser  == "U" or inputQuerySelectUser  == "u":
        inputIDUser = int(input(' ⊢ USER ID ... '))

        cursorCLI = mysqlCLI.cursor()
        if cursorCLI.execute(f"SELECT * FROM users WHERE id = {inputIDUser}"):
            cursorCLI.execute(f"DELETE FROM users WHERE id = {inputIDUser}")
            mysqlCLI.commit()

            print(Fore.LIGHTGREEN_EX + f"[✔] THE USER WAS REMOVED WITH ID {inputIDUser}." + Fore.WHITE + "\n")
        else:
            print(Fore.YELLOW + "[!] ID DO NOT EXIST." + Fore.WHITE + "\n")
    elif inputQuerySelectUser  == "TEACHER" or inputQuerySelectUser  == "teacher" or inputQuerySelectUser  == "T" or inputQuerySelectUser  == "t":
        inputIDTeachers = int(input(' ⊢ TEACHER ID ... '))

        cursorCLI = mysqlCLI.cursor()
        if cursorCLI.execute(f"SELECT * FROM teachers WHERE idTeachers = {inputIDTeachers}"):
            cursorCLI.execute(f"DELETE FROM teachers WHERE idTeachers = {inputIDTeachers}")
            mysqlCLI.commit()

            print(Fore.LIGHTGREEN_EX + f"[✔] THE TEACHER WAS REMOVED WITH ID {inputIDTeachers}." + Fore.WHITE + "\n")
        else:
            print(Fore.YELLOW + "[!] ID DO NOT EXIST." + Fore.WHITE + "\n")
    else:
        pass

while True:
    query = input('Please Select The Option: ')

    if int(query) == 0:
        create_admin_user()
    elif int(query) == 1:
        show_details_users()
    elif int(query) == 2:
        show_details_teachers()
    elif int(query) == 3:
        delete_user_teacher()
    elif int(query) == 4:
        mysqlCLI.close()
        break
    else:
        print(Fore.YELLOW + "[!] INVALID COMMAND." + Fore.WHITE)
