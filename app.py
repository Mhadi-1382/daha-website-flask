
'''
DAHA APPLICATION FLASK . V1.8.2
===============================

CREATED ON DATE: 1402/12/02
BUILT ON DATE: 1403/04/13

VIEW SOURCE CODE ON GITHUB: https://github.com/Mhadi-1382/daha-website-flask
'''

from flask import Flask, render_template, redirect, request, url_for, flash, session, send_from_directory, jsonify
from flask_mysqldb import MySQL
from fileinput import filename
from flask_sitemapper import Sitemapper
from flask_mail import Mail, Message

from send_notify import config_notify
# from task_scheduler import *
from api.api import APIRunning
from api.api_auth import auth

from persiantools.jdatetime import JalaliDateTime
from datetime import *
import random as rn
import os


# Version DAHA
_ver = "1.8.2"

web_url = "https://dahauni.ir/"
email_admin = ""
username_admin = ""
price_packages = ['50 هزار تومان']
number_card = ""

# Object flask app
app = Flask(__name__)
# Object DB (MySQL)
mysql = MySQL(app)
# Object sitemap.xml
sitemapper = Sitemapper()
sitemapper.init_app(app)

# Config DB
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'dahadb')

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
# app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.secret_key = os.urandom(24)

# Config MAIL SERVER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = f'{email_admin}'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = f'{email_admin}'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Object mail
mail = Mail(app)


@app.errorhandler(404)
def not_found_page(e):
    '''Error 404'''
    return render_template("404.html")


@app.route('/service-worker.js')
def serviceWorker():
    '''Service worker url'''
    return send_from_directory(app.static_folder, request.path[1:])
@app.route('/robots.txt')
def robots():
    '''Robots url'''
    return send_from_directory(app.static_folder, request.path[1:])
@app.route("/sitemap.xml/")
def sitemap():
    '''Sitemap'''
    return sitemapper.generate()


@sitemapper.include(lastmod="2024-03-02")
@app.route("/", methods=["GET"])
def index():
    '''Index'''
    # User check session
    if session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show alert
    cursor_alerts = mysql.connection.cursor()
    cursor_alerts.execute("SELECT * FROM alerts")

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("index.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_alerts=cursor_alerts.fetchall(), cursor_notifications_show=cursor_notifications_show.fetchall())


@sitemapper.include(lastmod="2024-03-27")
@app.route("/singup/", methods=["GET", "POST"])
def singup():
    '''Singup'''
    if request.method == "POST":
        username = request.form['userName']
        email = request.form['email']
        password = request.form['password']

        # Date & time
        dateSingup = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))

        cursor = mysql.connection.cursor()
        if (email) and cursor.execute("SELECT * FROM users WHERE email = %s", (email,)):
            flash('این ایمیل قبلا استفاده شده است.', 'error')
        elif (username) and cursor.execute("SELECT * FROM users WHERE userName = %s", (username,)):
            flash("این نام کاربری قبلا استفاده شده است.", 'error')
        # elif (password) and cursor.execute("SELECT * FROM users WHERE password = %s", (password,)):
        #     flash("این حساب کاربری نامعتبر است، رمز عبور خود را بررسی کنید.", 'error')
        else:
            cursor.execute("INSERT INTO users (userName, email, password, dateSingin) VALUES (%s,%s,%s,%s)", (username, email, password, dateSingup,))
            mysql.connection.commit()
            cursor.close()

            # Send email `Singup` for User
            msg = Message(
                subject= 'ثبت نام شما در داها با موفقیت انجام شد.',
                recipients= [email])
            msg.html = f"<div style='direction: rtl;'><p>{username} عزیز،</p><h4>حساب کاربری شما در داها با موفقیت ایجاد شد.</h4><br><h4>به جمع خانواده داها خوش آمدید، امیدواریم تجربه خوبی در پلتفرم داها داشته باشید.</h4><br><h3>مشخصات حساب کاربری</h3><p>نام کاربری: {username}</p><p>ایمیل: {email}</p><p>رمز عبور: {password}</p> <br> <h3>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)

            session['userName'] = username
            session['email'] = email
            session['password'] = password
            session.permanent = True

            return redirect("/")

    return render_template("singup.html")
@sitemapper.include(lastmod="2024-03-28")
@app.route("/login/", methods=["GET", "POST"])
def login():
    '''Login'''
    if request.method == "POST":
        username = request.form['userName']
        email = request.form['email']
        password = request.form['password']

        cursorStudent = mysql.connection.cursor()
        if cursorStudent.execute("SELECT * FROM users WHERE userName = %s AND email = %s AND password = %s", (username, email, password,)) and (username, email, password):
            session['userName'] = username
            session['email'] = email
            session['password'] = password
            session.permanent = True

            if username == username_admin and email == email_admin:
                return redirect("/admin")

            # cursorStudent.fetchone()

            return redirect("/")
        else:
            flash('ورود به سیستم انجام نشد، لطفا اطلاعات خود را بررسی کنید.', 'error')

    return render_template("login.html")
@app.route("/logout/")
def logout():
    '''Logout'''
    session.clear()

    return redirect("/")
@app.route("/user/forget_password/", methods=["GET", "POST"])
def forget_password():
    '''Forget password'''
    if request.method == "POST":
        email = request.form['email']

        cursor = mysql.connection.cursor()
        if cursor.execute("SELECT * FROM users WHERE email = %s", (email,)) and (email):
            return_password = cursor.fetchone()[3]
            flash('کاربر عزیز، رمز عبور به ایمیل شما ارسال شده است، ایمیل خود را بررسی کنید.', 'message')

            # Send email `Forget password` for User
            msg = Message(
                subject= 'بازیابی رمز عبور',
                recipients= [email])
            msg.html = f"<div style='direction: rtl;'><p>کاربر عزیز</p><h4>بازیابی رمز عبور با موفقیت انجام شده است.</h4> <br> <div style='margin: 1rem 0;font-size: 18px;font-weight: 700;border-bottom: 1px solid #808080;'>{return_password}</div> <br> <h3>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)

            return redirect("/login")
        else:
            flash('کاربری با این ایمیل یافت نشد.', 'error')

    return render_template("user/forget_password.html")
@app.route("/user/edit_info/", methods=["GET", "POST"])
def edit_info():
    '''Edit info'''
    if request.method == "POST":
        username = request.form['userName']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        if (username) and cursor.execute("SELECT * FROM users WHERE userName = %s", (username,)):
            flash("این نام کاربری قبلا استفاده شده است.", 'error')

            return redirect("/")
        elif session['email'] and cursor.execute("SELECT * FROM users WHERE email = %s", (session['email'],)):
            cursor.execute(f"UPDATE users SET userName = '{username}', password = '{password}' WHERE email = '{session['email']}'")
            mysql.connection.commit()
            cursor.close()

            session.clear()

    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")

    return redirect("/")
@app.route("/user/delete_account/", methods=["GET", "POST"])
def delete_account():
    '''Delete account'''
    cursor = mysql.connection.cursor()
    if session['email'] and session['userName']:
        cursor.execute("DELETE FROM users WHERE email = %s AND userName = %s", (session['email'], session['userName']))
        mysql.connection.commit()
        cursor.close()

        session.clear()

        # Send email to user
        msg = Message(
            subject= "حذف حساب کاربری در داها.",
            recipients= [session['email']])
        msg.html = f"<div style='direction: rtl;'><p>{session['userName']} عزیز،</p><h4>حساب کاربری شما با موفقیت در داها حذف شده است.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)

        return redirect("/singup/")

    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")
@app.route("/user/save_additional_info/", methods=["GET", "POST"])
def save_additional_info():
    '''Save additional info'''
    if request.method == "POST":
        number = request.form['number']
        uniqueCode = request.form['uniqueCode']
        dateBirth = request.form['dateBirth']
        major = request.form['major']
        education = request.form['education']
        job = request.form['job']
        interests = request.form['interests']

        cursor = mysql.connection.cursor()
        if session['email'] and cursor.execute("SELECT * FROM users WHERE email = %s", (session['email'],)):
            cursor.execute(f"UPDATE users SET number = '{number}', uniqueCode = '{uniqueCode}', dateBirth = '{dateBirth}', major = '{major}', education = '{education}', job = '{job}', interests = '{interests}' WHERE email = '{session['email']}'")
            mysql.connection.commit()
            cursor.close()

            session['number'] = number
            session['uniqueCode'] = uniqueCode
            session['dateBirth'] = dateBirth
            session['major'] = major
            session['education'] = education
            session['job'] = job
            session['interests'] = interests
            session.permanent = True

    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")

    return redirect("/")

@app.route("/login_teacher/", methods=["GET", "POST"])
def login_teacher():
    '''Login teacher'''
    if request.method == "POST":
        username = request.form['userName']
        email = request.form['email']
        password = request.form['password']
        teacherUniqueCode = request.form['teacherUniqueCode']

        cursorTeachers = mysql.connection.cursor()
        if cursorTeachers.execute("SELECT * FROM teachers WHERE userNameTeachers = %s AND emailTeachers = %s AND passwordTeachers = %s AND uniqueCodeTeachers = %s", (username, email, password, teacherUniqueCode,)) and (username, email, password, teacherUniqueCode):
            session['userName'] = username
            session['email'] = email
            session['password'] = password
            session['teacherUniqueCode'] = teacherUniqueCode
            session.permanent = True

            # cursorTeachers.fetchone()

            return redirect("/user/panel/teacher/")
        else:
            flash('ورود به سیستم انجام نشد، لطفا اطلاعات خود را بررسی کنید.', 'error')

    return redirect("/login/")
@app.route("/singup_teacher/", methods=["GET", "POST"])
def singup_teacher():
    '''Singup teacher'''
    if request.method == "POST":
        username = request.form['userName']
        email = request.form['email']
        password = request.form['password']
        teacherNumber = request.form['teacherNumber']
        teacherUniqueCode = request.form['teacherUniqueCode']

        # Secret key teachers (4-6 NUM)
        randomSecretKey = rn.randint(1001, 999999)

        # Date & time
        dateSingupTeachers = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))

        cursorTeachers = mysql.connection.cursor()
        if (email) and cursorTeachers.execute("SELECT * FROM teachers WHERE emailTeachers = %s", (email,)):
            flash('این ایمیل قبلا استفاده شده است.', 'error')
        elif (username) and cursorTeachers.execute("SELECT * FROM teachers WHERE userNameTeachers = %s", (username,)):
            flash("این نام کاربری قبلا استفاده شده است.", 'error')
        elif (teacherUniqueCode) and cursorTeachers.execute("SELECT * FROM teachers WHERE uniqueCodeTeachers = %s", (teacherUniqueCode,)):
            flash("این کد ملی قبلا استفاده شده است.", 'error')
        else:
            cursorTeachers.execute("INSERT INTO teachers (userNameTeachers, emailTeachers, passwordTeachers, numberTeachers, uniqueCodeTeachers, secretKeyTeachers, dateSinginTeachers) VALUES (%s,%s,%s,%s,%s,%s,%s)", (username, email, password, teacherNumber, teacherUniqueCode, randomSecretKey, dateSingupTeachers,))
            mysql.connection.commit()
            cursorTeachers.close()

            # Send email `Singup teacher`
            msg = Message(
                subject= 'ثبت نام شما در داها با موفقیت انجام شد.',
                recipients= [email])
            msg.html = f"<div style='direction: rtl;'><p> استاد عزیز {username}،</p><h4>حساب کاربری شما در داها با موفقیت ایجاد شد، بعد از تایید کلید امنیتی برای شما ایمیل می شود.</h4><br><h4>استاد گرامی، به جمع خانواده داها خوش آمدید، امیدواریم تجربه خوبی در پلتفرم داها داشته باشید.</h4><br><a href='{web_url}user/panel/teacher/'>داشبورد اساتید</a><br><h3>مشخصات حساب کاربری</h3><p>نام کاربری: {username}</p><p>کد ملی: {teacherUniqueCode}</p><p>شماره تلفن: {teacherNumber}</p><p>ایمیل: {email}</p><p>رمز عبور: {password}</p> <br> <h3>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)
            # Send email `Singup teacher` for Admin
            msg_admin = Message(
                subject= 'ثبت نام استاد جدید',
                recipients= [email_admin])
            msg_admin.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>استاد {username}، در داشبورد اساتید ثبت نام کردند، لطفا <a href='{web_url}admin/admin_users/'>وارد داشبورد</a> شوید و درخواست را بررسی کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_admin)

            session['userName'] = username
            session['email'] = email
            session['password'] = password
            session['teacherUniqueCode'] = teacherUniqueCode
            session.permanent = True

            return redirect("/user/panel/teacher/")

    return redirect("/singup/")
@app.route("/user/panel/edit_info/", methods=["GET", "POST"])
def panel_edit_info():
    '''Panel edit info'''
    if request.method == "POST":
        username = request.form['userName']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        if session['email'] and cursor.execute("SELECT * FROM teachers WHERE emailTeachers = %s", (session['email'],)):
            cursor.execute(f"UPDATE teachers SET userNameTeachers = '{username}', passwordTeachers = '{password}' WHERE emailTeachers = '{session['email']}'")
            mysql.connection.commit()
            cursor.close()

            session.clear()

    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")

    return redirect("/")
@app.route("/user/panel/delete_account/", methods=["GET", "POST"])
def panel_delete_account():
    '''Panel delete account'''
    cursor = mysql.connection.cursor()
    if session['email'] and session['userName']:
        cursor.execute("DELETE FROM teachers WHERE emailTeachers = %s AND userNameTeachers = %s", (session['email'], session['userName']))
        mysql.connection.commit()
        cursor.close()

        session.clear()

        # Send email to user
        msg = Message(
            subject= "حذف حساب کاربری در داها.",
            recipients= [session['email']])
        msg.html = f"<div style='direction: rtl;'><p>{session['userName']} عزیز،</p><h4>حساب کاربری شما با موفقیت در داها حذف شده است.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)

        return redirect("/singup/")

    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")
@app.route("/user/panel/save_additional_info/", methods=["GET", "POST"])
def panel_save_additional_info():
    '''Panel save additional info'''
    if request.method == "POST":
        dateBirth = request.form['dateBirth']
        major = request.form['major']
        education = request.form['education']
        job = request.form['job']
        interests = request.form['interests']

        cursor = mysql.connection.cursor()
        if session['email'] and cursor.execute("SELECT * FROM teachers WHERE emailTeachers = %s", (session['email'],)):
            cursor.execute(f"UPDATE teachers SET dateBirth = '{dateBirth}', major = '{major}', education = '{education}', job = '{job}', interests = '{interests}' WHERE emailTeachers = '{session['email']}'")
            mysql.connection.commit()
            cursor.close()

            session['dateBirth'] = dateBirth
            session['major'] = major
            session['education'] = education
            session['job'] = job
            session['interests'] = interests
            session.permanent = True

    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")

    return redirect("/")
@app.route("/user/panel/teacher/", methods=["GET", "POST"])
def panel_teacher():
    '''Panel teacher'''
    # User check session
    if session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    session_unique_code_teacher = session['teacherUniqueCode']
    
    # Show teachers
    cursor_teachers = mysql.connection.cursor()
    cursor_teachers.execute(f"SELECT * FROM teachers WHERE uniqueCodeTeachers = {session['teacherUniqueCode']}")
    show_teachers = cursor_teachers.fetchall()

    # Number publishers teacher
    number_publishers_teacher = cursor.execute(f"SELECT * FROM publishers WHERE uniqueCodeTeachers = {session['teacherUniqueCode']}")
    number_publishers_teacher = str(len(cursor.fetchall()))
    # Show publishers teacher
    cursor_publishers_teacher = mysql.connection.cursor()
    cursor_publishers_teacher.execute(f"SELECT * FROM publishers WHERE uniqueCodeTeachers = {session['teacherUniqueCode']}")
    show_publishers_teacher = cursor_publishers_teacher.fetchall()

    # Number teachers notifications
    number_teachers_notifications = cursor.execute(f"SELECT * FROM teachersnotifications WHERE uniqueCodeTeachersNotifications = {session['teacherUniqueCode']}")
    number_teachers_notifications = str(len(cursor.fetchall()))
    # Show teachers notifications
    cursor_teachers_notifications = mysql.connection.cursor()
    cursor_teachers_notifications.execute(f"SELECT * FROM teachersnotifications WHERE uniqueCodeTeachersNotifications = {session['teacherUniqueCode']}")
    show_teachers_notifications = cursor_teachers_notifications.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("user/panel/teacher.html", _ver=_ver, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, session_unique_code_teacher=session_unique_code_teacher, number_publishers_teacher=number_publishers_teacher, show_publishers_teacher=show_publishers_teacher, number_teachers_notifications=number_teachers_notifications, show_teachers_notifications=show_teachers_notifications, show_teachers=show_teachers, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/user/panel/teacher/publishers/", methods=["GET", "POST"])
def panel_teachers_publishers():
    '''Teachers publishers'''
    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")
        
    if request.method == "POST":
        titleHandout = request.form.get('titleHandout')
        linkHandout = request.form.get('linkHandout')

        # Date & time
        datePublishers = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_publishers = mysql.connection.cursor()
        if cursor_publishers:
            cursor_publishers.execute("INSERT INTO publishers (titleHandout, linkHandout, datePublishers, uniqueCodeTeachers) VALUES (%s,%s,%s,%s)", (titleHandout, linkHandout, datePublishers, session['teacherUniqueCode'],))
            mysql.connection.commit()
            cursor_publishers.close()

    return redirect("/user/panel/teacher/")
@app.route("/user/panel/delete_publisher_teacher/<int:id>", methods=["GET", "POST"])
def panel_delete_publisher_teacher(id):
    '''Delete publisher teacher'''
    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM publishers WHERE idPublishers = {}'.format(id))
        mysql.connection.commit()
    
        return redirect("/user/panel/teacher/")
    elif request.method == "GET":
        return redirect("/")
@app.route("/user/panel/teacher/notifications/", methods=["GET", "POST"])
def panel_teachers_notifications():
    '''Teachers notifications'''
    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")

    if request.method == "POST":
        nameAndClassTeachersNotifications = request.form.get('nameAndClassTeachersNotifications')
        titleTeachersNotifications = request.form.get('titleTeachersNotifications')
        desTeachersNotifications = request.form.get('desTeachersNotifications')

        # Date & time
        dateNotifications = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_teachers_notifications = mysql.connection.cursor()
        if cursor_teachers_notifications:
            cursor_teachers_notifications.execute("INSERT INTO teachersnotifications (nameAndClassTeachersNotifications, titleTeachersNotifications, desTeachersNotifications, dateTeachersNotifications, uniqueCodeTeachersNotifications) VALUES (%s,%s,%s,%s,%s)", (nameAndClassTeachersNotifications, titleTeachersNotifications, desTeachersNotifications, dateNotifications, session['teacherUniqueCode'],))
            mysql.connection.commit()

            # Send email to user & Send notify API & Save to Teachers notifications
            try:
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT email FROM users")
                email_flags = cursor.fetchall()
                for email in email_flags:
                    msg_users = Message(
                        subject= titleTeachersNotifications,
                        recipients= [email[0]])
                    msg_users.html = f"<div style='direction: rtl;'><p style='font-size: 1rem;'>{nameAndClassTeachersNotifications} <br> {titleTeachersNotifications} <br> {desTeachersNotifications}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
                    mail.send(msg_users)
                
                notifyUrlIcon = "https://dahauni.ir/static/media/images/icon.svg"
                notifyUrlLink = "https://dahauni.ir/"
                
                config_notify(titleTeachersNotifications, desTeachersNotifications, notifyUrlIcon, notifyUrlLink)
            except:
                flash("ارسال اعلان با مشکل مواجه شده است، لطفا مجدد امتحان نمایید.")
            
            cursor_teachers_notifications.close()

    return redirect("/user/panel/teacher/")
@app.route("/user/panel/delete_teachers_notifications/<int:id>", methods=["GET", "POST"])
def panel_delete_teachers_notifications(id):
    '''Delete teachers notifications'''
    # User check session
    if session.values():
        session['email']
        session['userName']
    else:
        return redirect("/login")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM teachersnotifications WHERE idTeachersNotifications = {}'.format(id))
        mysql.connection.commit()
    
        return redirect("/user/panel/teacher/")
    elif request.method == "GET":
        return redirect("/")


@app.route("/admin/", methods=["GET", "POST"])
def admin():
    '''Admin dashbord'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # Show 8 user
    cursor_user_show = mysql.connection.cursor()
    cursor_user_show.execute('SELECT * FROM users')
    # Show 8 comment
    cursor_comment_show = mysql.connection.cursor()
    cursor_comment_show.execute('SELECT * FROM comment')
    # Show 8 technologist
    cursor_technologist_show = mysql.connection.cursor()
    cursor_technologist_show.execute("SELECT * FROM technologistget")
    # Show 8 events
    cursor_events_show = mysql.connection.cursor()
    cursor_events_show.execute("SELECT * FROM events")
    # Show 8 sites
    cursor_sites_show = mysql.connection.cursor()
    cursor_sites_show.execute("SELECT * FROM sites")
    # Show 8 publishers
    cursor_publishers_show = mysql.connection.cursor()
    cursor_publishers_show.execute("SELECT * FROM publishers")
    # Show 8 ticket
    cursor_ticket_show = mysql.connection.cursor()
    cursor_ticket_show.execute('SELECT * FROM ticket')
    # Show 8 teachers
    cursor_teachers_show = mysql.connection.cursor()
    cursor_teachers_show.execute('SELECT * FROM teachers')
    # Show 8 teachers
    cursor_teachers_notifications_show = mysql.connection.cursor()
    cursor_teachers_notifications_show.execute('SELECT * FROM teachersnotifications')
    # Show 8 notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")
    # Show 8 api
    cursor_api_show = mysql.connection.cursor()
    cursor_api_show.execute("SELECT * FROM api")

    # Number users
    cursor_user = mysql.connection.cursor()
    cursor_user.execute('SELECT * FROM users')
    number_users = int(len(cursor_user.fetchall()))
    # Number comments
    cursor_comment = mysql.connection.cursor()
    cursor_comment.execute('SELECT * FROM comment')
    number_comments = str(len(cursor_comment.fetchall()))
    # Number technologist get
    cursor_technologist = mysql.connection.cursor()
    cursor_technologist.execute('SELECT * FROM technologistget')
    number_technologists = str(len(cursor_technologist.fetchall()))
    # Number technologist set
    cursor_technologist_set = mysql.connection.cursor()
    cursor_technologist_set.execute('SELECT * FROM technologistset')
    number_technologists_set = str(len(cursor_technologist_set.fetchall()))
    # Number events
    cursor_events = mysql.connection.cursor()
    cursor_events.execute('SELECT * FROM events')
    number_events = str(len(cursor_events.fetchall()))
    # Number sites
    cursor_sites = mysql.connection.cursor()
    cursor_sites.execute('SELECT * FROM sites')
    number_sites = str(len(cursor_sites.fetchall()))
    # Number publishers
    cursor_publishers = mysql.connection.cursor()
    cursor_publishers.execute('SELECT * FROM publishers')
    number_publishers = str(len(cursor_publishers.fetchall()))
    # Number ticket
    cursor_ticket = mysql.connection.cursor()
    cursor_ticket.execute('SELECT * FROM ticket')
    number_ticket = str(len(cursor_ticket.fetchall()))
    # Number teachers
    cursor_teachers = mysql.connection.cursor()
    cursor_teachers.execute('SELECT * FROM teachers')
    number_teachers = int(len(cursor_teachers.fetchall()))
    # Number teachers notifications
    cursor_teachers_notifications = mysql.connection.cursor()
    cursor_teachers_notifications.execute('SELECT * FROM teachersnotifications')
    number_teachers_notifications = int(len(cursor_teachers_notifications.fetchall()))
    # Number notifications
    number_notifications = mysql.connection.cursor()
    number_notifications.execute('SELECT * FROM notifications')
    number_notifications = str(len(number_notifications.fetchall()))
    # Number api
    number_api = mysql.connection.cursor()
    number_api.execute('SELECT * FROM api')
    number_api = str(len(number_api.fetchall()))

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show email users
    show_email_users = mysql.connection.cursor()
    show_email_users.execute('SELECT * FROM users')
    
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin.html", _ver=_ver, email_admin=email_admin, number_users=number_users, number_comments=number_comments, users=cursor_user_show.fetchall(), comments=cursor_comment_show.fetchall(), session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_technologist_show=cursor_technologist_show.fetchall(), number_technologists=number_technologists, number_technologists_set=number_technologists_set, cursor_events_show=cursor_events_show.fetchall(), number_events=number_events, cursor_sites_show=cursor_sites_show.fetchall(), number_sites=number_sites, cursor_publishers_show=cursor_publishers_show.fetchall(), number_publishers=number_publishers, cursor_ticket_show=cursor_ticket_show.fetchall(), number_ticket=number_ticket, show_email_users=show_email_users, return_title_ad=return_title_ad, cursor_teachers_show=cursor_teachers_show.fetchall(), number_teachers=number_teachers, cursor_teachers_notifications_show=cursor_teachers_notifications_show.fetchall(), number_teachers_notifications=number_teachers_notifications, number_notifications=number_notifications, cursor_notifications_show=cursor_notifications_show.fetchall(), cursor_api_show=cursor_api_show.fetchall(), number_api=number_api, pricePackages=price_packages)

@app.route("/admin/admin_users/", methods=["GET", "POST"])
def admin_users():
    '''Admin Users'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")
    
    # Show users
    cursor_user_show = mysql.connection.cursor()
    cursor_user_show.execute('SELECT * FROM users')
    # Number users
    cursor_user = mysql.connection.cursor()
    cursor_user.execute('SELECT * FROM users')
    number_users = str(len(cursor_user.fetchall()))

    # Show teachers
    cursor_teachers_show = mysql.connection.cursor()
    cursor_teachers_show.execute('SELECT * FROM teachers')
    # Number teachers
    cursor_teachers = mysql.connection.cursor()
    cursor_teachers.execute('SELECT * FROM teachers')
    number_teachers = str(len(cursor_teachers.fetchall()))

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
            
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_users.html", _ver=_ver, email_admin=email_admin, users=cursor_user_show.fetchall(), session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, number_users=number_users, return_title_ad=return_title_ad, cursor_teachers_show=cursor_teachers_show.fetchall(), number_teachers=number_teachers, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/delete_users/<int:id>", methods=["GET", "POST"])
def delete_users(id):
    '''Delete users'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM users WHERE id = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_users')
    elif request.method == "GET":
        return redirect("/")
@app.route("/delete_teacher/<int:id>", methods=["GET", "POST"])
def delete_teacher(id):
    '''Delete teacher'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM teachers WHERE idTeachers = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_users')
    elif request.method == "GET":
        return redirect("/")
@app.route("/accept_teacher/<int:id>", methods=["GET", "POST"])
def accept_teacher(id):
    '''Accept teacher'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")
        
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('SELECT emailTeachers FROM teachers WHERE idTeachers = {}'.format(id))
        
        cur_username = mysql.connection.cursor()
        cur_username.execute('SELECT userNameTeachers FROM teachers WHERE idTeachers = {}'.format(id))

        cur_secret_key = mysql.connection.cursor()
        cur_secret_key.execute('SELECT secretKeyTeachers FROM teachers WHERE idTeachers = {}'.format(id))

        # Send email `Api` for Teacher
        msg_ = Message(
            subject= 'تایید حساب و کلید امنیتی شما در داها.',
            recipients= [f'{cur.fetchone()[0]}'])
        msg_.html = f"<div style='direction: rtl;'><p>استاد عزیز {cur_username.fetchone()[0]}،</p><br><h4>حساب شما در داها با موفقیت تایید شد، کلید امنیتی شما برای ورود به داشبورد:</h4><div style='margin: 1rem 0;font-size: 18px;font-weight: 700;border-bottom: 1px solid #808080;'>{cur_secret_key.fetchone()[0]}</div> <br> <h4>به جمع خانواده داها خوش آمدید، امیدواریم تجربه خوبی در پلتفرم داها داشته باشید.</h4> <br> <h3>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg_)
    
        return redirect('/admin/admin_users')
    elif request.method == "GET":
        return redirect("/")

@app.route("/admin/admin_comments/")
def admin_comments():
    '''Admin Comments'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")
        
    cursor_comment = mysql.connection.cursor()
    cursor_comment.execute('SELECT * FROM comment')

    # Number comments
    cursor_comment_show = mysql.connection.cursor()
    cursor_comment_show.execute('SELECT * FROM comment')
    number_comments = str(len(cursor_comment.fetchall()))

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
        
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_comments.html", _ver=_ver, email_admin=email_admin, comments=cursor_comment_show.fetchall(), session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, number_comments=number_comments, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/delete_comments/<int:id>", methods=["GET", "POST"])
def delete_comments(id):
    '''Delete comments'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM comment WHERE idComment = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_comments')
    elif request.method == "GET":
        return redirect("/")
@app.route("/user/comment/", methods=["GET", "POST"])
def comment():
    '''Comment'''
    if request.method == "POST":
        username = request.form.get('userName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        # Date & time
        datetime = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))

        cursor = mysql.connection.cursor()
        if cursor:
            cursor.execute("INSERT INTO comment (userName, email, phone, message, dateMessage) VALUES (%s,%s,%s,%s,%s)", (username, email, phone, message, datetime,))
            mysql.connection.commit()
            cursor.close()

            # Send email `Comment` for Admin
            msg_admin = Message(
                subject= 'ثبت نظر جدید',
                recipients= [email_admin])
            msg_admin.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>کاربر {username}، یک نظر ارسال کردند.</h4><h3>متن پیام</h3><p>{message}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_admin)
        
            return redirect("/")
        else:
            flash("ارسال پیام شما با مشکل مواجه شده است، لطفا ورودی را بررسی کنید.", 'error')

    return redirect("/")

@app.route("/admin/admin_files/", methods=["GET", "POST"])
def admin_files():
    '''Admin file'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show files uploaded
    path_folder_files_uploaded = os.listdir("static/media/uploads/")

    # Number files
    number_files = str(len(path_folder_files_uploaded))
                
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_files.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, path_folder_files_uploaded=path_folder_files_uploaded, number_files=number_files, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/delete_admin_files/<file>", methods=["GET", "POST"])
def delete_admin_files(file):
    '''Delete files'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        os.remove("static/media/uploads/{}".format(file))
    
        return redirect('/admin/admin_files')
    elif request.method == "GET":
        return redirect("/")
@app.route("/upload_file/", methods=["GET", "POST"])
def upload_file():
    '''Upload file'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        uploadFile = request.files.get('uploadFile')

        # Upload & rename file
        try:
            uploadFile.save(uploadFile.filename)
            os.rename(uploadFile.filename, f'./static/media/uploads/{uploadFile.filename}')
            
            return redirect("/admin/")
        except:
            flash("بارگذاری فایل با مشکل مواجه شده است، لطفا مجدد امتحان نمایید.")
    elif request.method == "GET":
        return redirect("/")

@app.route("/admin/admin_technologist/", methods=["GET", "POST"])
def admin_technologist():
    '''Admin technologist'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show technologist
    cursor_technologist_show = mysql.connection.cursor()
    cursor_technologist_show.execute("SELECT * FROM technologistget")
    cursor_technologist_set_show = mysql.connection.cursor()
    cursor_technologist_set_show.execute("SELECT * FROM technologistset")

    # Number technologists
    cursor_technologist = mysql.connection.cursor()
    cursor_technologist.execute('SELECT * FROM technologistget')
    number_technologists = str(len(cursor_technologist.fetchall()))
    cursor_technologist_set = mysql.connection.cursor()
    cursor_technologist_set.execute('SELECT * FROM technologistset')
    number_technologists_set = str(len(cursor_technologist_set.fetchall()))
                    
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_technologist.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_technologist_show=cursor_technologist_show.fetchall(), cursor_technologist_set_show=cursor_technologist_set_show.fetchall(), number_technologists=number_technologists, number_technologists_set=number_technologists_set, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/pages/technologist_set/", methods=["GET", "POST"])
def technologist_set():
    '''Technologist set'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        fileUrlTechnologist = request.form.get('fileUrlTechnologist')
        usernameTechnologist = request.form.get('usernameTechnologist')
        titleTechnologist = request.form.get('titleTechnologist')
        titleJobTechnologist = request.form.get('titleJobTechnologist')
        emailTechnologist = request.form.get('emailTechnologist')
        phoneTechnologist = request.form.get('phoneTechnologist')
        categoryTechnologist = request.form.get('categoryTechnologist')
        addressTechnologist = request.form.get('addressTechnologist')
        desTechnologist = request.form.get('desTechnologist')
        selectExpirTechnologist = request.form.get('selectExpirTechnologist')

        # Date & time
        dateTechnologist = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_technologist = mysql.connection.cursor()
        if cursor_technologist:
            cursor_technologist.execute("INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist,))
            mysql.connection.commit()
            cursor_technologist.close()

            # Send email `Technologist set`
            msg = Message(
                subject= 'آگهی شما با موفقیت در داها ثبت شد.',
                recipients= [emailTechnologist])
            msg.html = f"<div style='direction: rtl;'><p>{usernameTechnologist} عزیز تبریک،</p><h4>درخواست شما برای ثبت آگهی در داها بررسی و هم اکنون در بخش فن آور اضافه شده است.</h4><br><h3>مشخصات آگهی شما</h3><img src='{fileUrlTechnologist}' alt='{fileUrlTechnologist}'  style='width: 50px;height: 50px;border-radius: 9999px;'><p>نام و نام خانوادگی: {usernameTechnologist}</p><p>عنوان آکهی: {titleTechnologist}</p><p>نوع آگهی: {titleJobTechnologist}</p><p>ایمیل: {emailTechnologist}</p><p>شماره تماس: {phoneTechnologist}</p><p>دسته بندی: {categoryTechnologist}</p><p>آدرس محل کار: {addressTechnologist}</p><p>توضیحات: {desTechnologist}</p> <br> <p>تاریخ ثبت آگهی: {dateTechnologist}</p> <p>بسته: {selectExpirTechnologist}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)

        return redirect("/pages/technologist")
    
    return render_template("pages/technologist.html")
@app.route("/delete_technologists_set_ad/<int:id>", methods=["GET", "POST"])
def delete_technologists_set_ad(id):
    '''Delete technologists set ad'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        # Send email `Delete technologists set ad`
        cur_email_user = mysql.connection.cursor()
        cur_email_user.execute('SELECT emailTechnologist FROM technologistset WHERE idTechnologist = {}'.format(id))
        emailTechnologist = cur_email_user.fetchone()

        cur_title = mysql.connection.cursor()
        cur_title.execute('SELECT titleTechnologist FROM technologistset WHERE idTechnologist = {}'.format(id))

        cur_change_status = mysql.connection.cursor()
        cur_change_status.execute('UPDATE technologistget SET statusTechnologist = "نامعتبر" WHERE idTechnologist = "{}"'.format(id))
        mysql.connection.commit()

        b = cur_title.fetchone()[0]
        
        msg = Message(
            subject= f'بسته آگهی {b} در داها  به پایان رسیده است.',
            recipients= [str(emailTechnologist[0])])
        msg.html = f"<div style='direction: rtl;'><p>{str(emailTechnologist[0])} عزیز،</p><h4>بسته آگهی {b} در داها به پایان رسیده است،</h4><h4>برای تمدید مجدد میتوانید درخواست خود را دوباره ارسال و یا با پشتیبانی ارتباط برقرار کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistset WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')
    elif request.method == "GET":
        return redirect("/")
@app.route("/delete_technologists_get_ad/<int:id>", methods=["GET", "POST"])
def delete_technologists_get_ad(id):
    '''Delete technologists get ad'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        # Send email `Delete technologists get ad`
        cur_email_user = mysql.connection.cursor()
        cur_email_user.execute('SELECT emailTechnologist FROM technologistget WHERE idTechnologist = {}'.format(id))
        emailTechnologist = cur_email_user.fetchone()

        cur_change_status = mysql.connection.cursor()
        cur_change_status.execute('UPDATE technologistget SET statusTechnologist = "رد شده" WHERE idTechnologist = "{}"'.format(id))
        mysql.connection.commit()
        
        msg = Message(
            subject= 'آگهی شما در داها تایید نشده است.',
            recipients= [str(emailTechnologist[0])])
        msg.html = f"<div style='direction: rtl;'><p>{str(emailTechnologist[0])} عزیز متاسفانه،</p><h4>درخواست شما برای ثبت آگهی رد شده است،</h4><h4>در صورت نیاز کارشناسان ما با شما تماس خواهند گرفت.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistget WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')
    elif request.method == "GET":
        return redirect("/")
@app.route("/delete_technologists_get/<int:id>", methods=["GET", "POST"])
def delete_technologists_get(id):
    '''Delete technologists get'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistget WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')
    elif request.method == "GET":
        return redirect("/")
@app.route("/delete_technologists_set/<int:id>", methods=["GET", "POST"])
def delete_technologists_set(id):
    '''Delete technologists set'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistset WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')
    elif request.method == "GET":
        return redirect("/")
@app.route("/accept_technologists_get/<int:id>", methods=["GET", "POST"])
def accept_technologists_get(id):
    '''Accept technologists get'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur_email = mysql.connection.cursor()
        cur_email.execute('SELECT emailTechnologist FROM technologistget WHERE idTechnologist = "{}"'.format(id))

        cur_username = mysql.connection.cursor()
        cur_username.execute('SELECT usernameTechnologist FROM technologistget WHERE idTechnologist = "{}"'.format(id))

        cur_title = mysql.connection.cursor()
        cur_title.execute('SELECT titleTechnologist FROM technologistget WHERE idTechnologist = "{}"'.format(id))

        cur_change_status = mysql.connection.cursor()
        cur_change_status.execute('UPDATE technologistget SET statusTechnologist = "تایید شده و پرداخت" WHERE idTechnologist = "{}"'.format(id))
        mysql.connection.commit()

        # Send email `Accept technologist get`
        msg = Message(
            subject= 'آگهی شما در داها تایید و در انتظار پرداخت می باشد.',
            recipients= [f'{cur_email.fetchone()[0]}'])
        msg.html = f"<div style='direction: rtl;'><p>{cur_username.fetchone()[0]} عزیز،</p><h4>درخواست شما برای ثبت آگهی تحت عنوان {cur_title.fetchone()[0]} در داها تایید و هم اکنون در انتظار پرداخت می باشد، جهت پرداخت از طریق شماره کارت (بانک سپه، محمد مهدی ربیعی) زیر اقدام و فیش پرداختی را در شبکه های اجتماعی (ایتا، تلگرام) به این شماره <a href='tel:09031265448'>09031265448</a> ارسال کنید، همچنین میتوانید از طریق تماس تلفنی یا پیامک هم اطلاع بدهید. <span style='margin: 1rem 0;font-size: 18px;font-weight: 700;border-bottom: 1px solid #808080;'>{number_card}</span></h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)
    
        return redirect('/admin/admin_technologist')
    elif request.method == "GET":
        return redirect("/")
@app.route("/record_technologists_get/<int:id>", methods=["GET", "POST"])
def record_technologists_get(id):
    '''Record technologists get'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur_email = mysql.connection.cursor()
        cur_email.execute('SELECT emailTechnologist FROM technologistget WHERE idTechnologist = "{}"'.format(id))

        cur_username = mysql.connection.cursor()
        cur_username.execute('SELECT usernameTechnologist FROM technologistget WHERE idTechnologist = "{}"'.format(id))

        cur_title = mysql.connection.cursor()
        cur_title.execute('SELECT titleTechnologist FROM technologistget WHERE idTechnologist = "{}"'.format(id))

        cur_read_data = mysql.connection.cursor()
        cur_read_data.execute('SELECT * FROM technologistget WHERE idTechnologist = "{}"'.format(id))
        cur_record = mysql.connection.cursor()
        for show_read_data in cur_read_data.fetchall():
            if show_read_data[11] == "1":
                if show_read_data[10][5:7] == "09":
                    dateExpirTechnologist = show_read_data[10][0:5] + "10" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()
                elif show_read_data[10][5:6] == "0":
                    dateExpirTechnologist = show_read_data[10][0:5] + f"0{int(show_read_data[10][6:7]) + 1}" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()
                elif show_read_data[10][5:7] == "12":
                    dateExpirTechnologist = show_read_data[10][0:3] + f"{int(show_read_data[10][3:4]) + 1}-" + "01" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()
                else:
                    dateExpirTechnologist = show_read_data[10][0:5] + f"{int(show_read_data[10][5:7]) + 1}" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()
            elif show_read_data[11] == "2":
                if show_read_data[10][5:7] == "09":
                    dateExpirTechnologist = show_read_data[10][0:5] + "10" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()
                elif show_read_data[10][5:6] == "0":
                    dateExpirTechnologist = show_read_data[10][0:5] + f"0{int(show_read_data[10][6:7]) + 1}" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()
                elif show_read_data[10][5:7] == "12":
                    dateExpirTechnologist = show_read_data[10][0:3] + f"{int(show_read_data[10][3:4]) + 1}-" + "01" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()
                else:
                    dateExpirTechnologist = show_read_data[10][0:5] + f"{int(show_read_data[10][5:7]) + 1}" + show_read_data[10][7:10]
                    cur_record.execute('INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, dateExpirTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (show_read_data[1], show_read_data[2], show_read_data[3], show_read_data[4], show_read_data[5], show_read_data[6], show_read_data[7], show_read_data[8], show_read_data[9], show_read_data[10], show_read_data[11], dateExpirTechnologist,))
                    mysql.connection.commit()

        cur_change_status = mysql.connection.cursor()
        cur_change_status.execute('UPDATE technologistget SET statusTechnologist = "ثبت شده" WHERE idTechnologist = "{}"'.format(id))
        mysql.connection.commit()

        # Send email `Record technologist get`
        msg = Message(
            subject= 'تبریک آگهی شما با موفقیت در داها ثبت و منتشر شده.',
            recipients= [f'{cur_email.fetchone()[0]}'])
        msg.html = f"<div style='direction: rtl;'><p>{cur_username.fetchone()[0]} عزیز تبریک،</p><h4>آگهی شما تحت عنوان {cur_title.fetchone()[0]} در داها ثبت و منتشر شده، هم اکنون در قسمت فن آور قابل رویت می باشد.</h4><h4>آدرس آگهی شما</h4><h4><a href='{web_url}pages/technologist/#id={id}'>{web_url}pages/technologist/#id={id}</a></h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)

        return redirect('/admin/admin_technologist')
    elif request.method == "GET":
        return redirect("/")

@app.route("/admin/admin_events/", methods=["GET", "POST"])
def admin_events():
    '''Admin events'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show events
    cursor_events_show = mysql.connection.cursor()
    cursor_events_show.execute("SELECT * FROM events")

    # Number events
    cursor_events = mysql.connection.cursor()
    cursor_events.execute('SELECT * FROM events')
    number_events = str(len(cursor_events.fetchall()))
                        
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_events.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_events_show=cursor_events_show.fetchall(), number_events=number_events, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/delete_events/<int:id>", methods=["GET", "POST"])
def delete_events(id):
    '''Delete events'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM events WHERE idEvents = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_events')
    elif request.method == "GET":
        return redirect("/")

@app.route("/admin/admin_sites/", methods=["GET", "POST"])
def admin_sites():
    '''Admin sites'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show sites
    cursor_sites_show = mysql.connection.cursor()
    cursor_sites_show.execute("SELECT * FROM sites")

    # Number sites
    cursor_sites = mysql.connection.cursor()
    cursor_sites.execute('SELECT * FROM sites')
    number_sites = str(len(cursor_sites.fetchall()))
                            
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_sites.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_sites_show=cursor_sites_show.fetchall(), number_sites=number_sites, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/delete_sites/<int:id>", methods=["GET", "POST"])
def delete_sites(id):
    '''Delete sites'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM sites WHERE idSites = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_sites')
    elif request.method == "GET":
        return redirect("/")

@app.route("/admin/admin_publishers/", methods=["GET", "POST"])
def admin_publishers():
    '''Admin publishers'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show publishers
    cursor_publishers_show = mysql.connection.cursor()
    cursor_publishers_show.execute("SELECT * FROM publishers")

    # Number publishers
    number_publishers = mysql.connection.cursor()
    number_publishers.execute('SELECT * FROM publishers')
    number_publishers = str(len(number_publishers.fetchall()))
                                
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_publishers.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_publishers_show=cursor_publishers_show.fetchall(), number_publishers=number_publishers, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/delete_publisher/<int:id>", methods=["GET", "POST"])
def delete_publisher(id):
    '''Delete publisher'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM publishers WHERE idPublishers = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_publishers')
    elif request.method == "GET":
        return redirect("/")

@app.route("/admin/admin_ticket/", methods=["GET", "POST"])
def admin_ticket():
    '''Admin ticket'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show ticket
    cursor_ticket_show = mysql.connection.cursor()
    cursor_ticket_show.execute("SELECT * FROM ticket")

    # Number ticket
    number_ticket = mysql.connection.cursor()
    number_ticket.execute('SELECT * FROM ticket')
    number_ticket = str(len(number_ticket.fetchall()))

    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_ticket.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_ticket_show=cursor_ticket_show.fetchall(), number_ticket=number_ticket, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/answer_ticket/<int:id>", methods=["GET", "POST"])
def answer_ticket(id):
    '''Answer ticket'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        titleTicket = request.form.get('titleTicket')
        answerTicket = request.form.get('answerTicket')

        cur = mysql.connection.cursor()
        if cur:
            cur.execute('UPDATE ticket SET answerTicket = "{}" WHERE idTicket = {}'.format(answerTicket, id))
            mysql.connection.commit()

            cur_username = mysql.connection.cursor()
            cur_username.execute('SELECT usernameTicket FROM ticket WHERE idTicket = {}'.format(id))

            cur_email = mysql.connection.cursor()
            cur_email.execute('SELECT emailTicket FROM ticket WHERE idTicket = {}'.format(id))

            # Send email `Answer Ticket` for User
            msg_ = Message(
                subject= f'ثبت پاسخ برای تیکت شما با موضوع {titleTicket}.',
                recipients= [cur_email.fetchone()[0]])
            msg_.html = f"<div style='direction: rtl;'><p>{cur_username.fetchone()[0]} عزیز سلام،</p><h3>پاسخ تیکت شما با موضوع {titleTicket}:</h3><p>{answerTicket}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_)
        
            return redirect('/admin/admin_ticket')
    elif request.method == "GET":
        return redirect("/")
@app.route("/delete_ticket/<int:id>", methods=["GET", "POST"])
def delete_ticket(id):
    '''Delete ticket'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM ticket WHERE idTicket = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_ticket')
    elif request.method == "GET":
        return redirect("/")
@app.route("/user/ticket/", methods=["GET", "POST"])
def ticket():
    '''Ticket'''
    if request.method == "POST":
        usernameTicket = request.form.get('usernameTicket')
        titleTicket = request.form.get('titleTicket')
        emailTicket = request.form.get('emailTicket')
        messageTicket = request.form.get('messageTicket')

        # Date & time
        dateTicket = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))

        cursor = mysql.connection.cursor()
        if cursor:
            cursor.execute("INSERT INTO ticket (usernameTicket, titleTicket, emailTicket, messageTicket, dateTicket) VALUES (%s,%s,%s,%s,%s)", (usernameTicket, titleTicket, emailTicket, messageTicket, dateTicket,))
            mysql.connection.commit()
            cursor.close()

            # Send email `Ticket` for User
            msg_admin = Message(
                subject= f'ثبت تیکت با موضوع {titleTicket}.',
                recipients= [emailTicket])
            msg_admin.html = f"<div style='direction: rtl;'><p>{usernameTicket} عزیز سلام،</p><h4>تیکت شما با موضوع {titleTicket} در داها ثبت شد. لطفا کمی شکیبا باشید تا پاسخ برایتان ارسال شود.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_admin)
            # Send email `Ticket` for Admin
            msg_admin = Message(
                subject= 'ثبت تیکت جدید',
                recipients= [email_admin])
            msg_admin.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>کاربر {usernameTicket}، یک تیکت ارسال کردند، جهت ثبت پاسخ <a href='{web_url}admin/admin_ticket/'>وارد داشبورد</a> شوید.</h4><h4>عنوان تیکت: </h4><p>{titleTicket}</p><h4>متن تیکت: </h4><p>{messageTicket}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_admin)
        
            return redirect("/")
        else:
            flash("ارسال تیکت شما با مشکل مواجه شده است، لطفا ورودی را بررسی کنید.", 'error')

    return redirect("/")

@app.route("/admin/admin_teachers_notifications/", methods=["GET", "POST"])
def admin_teachers_notifications():
    '''Admin teachers notifications'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show teachers notifications
    cursor_teachers_notifications_show = mysql.connection.cursor()
    cursor_teachers_notifications_show.execute("SELECT * FROM teachersnotifications")

    # Number teachers notifications
    number_teachers_notifications = mysql.connection.cursor()
    number_teachers_notifications.execute('SELECT * FROM teachersnotifications')
    number_teachers_notifications = str(len(number_teachers_notifications.fetchall()))

    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("admin/admin_teachers_notifications.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_teachers_notifications_show=cursor_teachers_notifications_show.fetchall(), number_teachers_notifications=number_teachers_notifications, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/delete_teachers_notifications/<int:id>", methods=["GET", "POST"])
def delete_teachers_notifications(id):
    '''Delete teachers notifications'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM teachersnotifications WHERE idTeachersNotifications = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_teachers_notifications')
    elif request.method == "GET":
        return redirect("/")

@app.route("/admin/admin_send_email/", methods=["GET", "POST"])
def admin_send_email():
    '''Admin-Send email'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")
        
    if request.method == "POST":
        emailTo = request.form['emailTo']
        emailSubject = request.form['emailSubject']
        emailMessage = request.form['emailMessage']
        
        sendAllEmail = request.form.getlist('sendAllEmail')

        # Send email to user
        try:
            if sendAllEmail:
                cursor = mysql.connection.cursor()
                cursor.execute("SELECT email FROM users")
                email_flags = cursor.fetchall()
                for email in email_flags:
                    msg_users = Message(
                        subject= emailSubject,
                        recipients= [email[0]])
                    msg_users.html = f"<div style='direction: rtl;'><p style='font-size: 1rem;'>{emailMessage}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
                    mail.send(msg_users)
            else:
                msg_user = Message(
                    subject= emailSubject,
                    recipients= [emailTo])
                msg_user.html = f"<div style='direction: rtl;'><p style='font-size: 1rem;'>{emailMessage}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
                mail.send(msg_user)
        except:
            flash("ارسال ایمیل با مشکل مواجه شده است، لطفا مجدد امتحان نمایید.")

    return redirect("/admin")

@app.route("/admin/admin_send_alert/", methods=["GET", "POST"])
def admin_send_alert():
    '''Admin-Send alert'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        titleAlert = request.form['titleAlert']
        contentAlert = request.form['contentAlert']

        # Date & time
        dateAlert = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_alerts = mysql.connection.cursor()
        if cursor_alerts:
            cursor_alerts.execute("INSERT INTO alerts (titleAlert, contentAlert, dateAlert) VALUES (%s,%s,%s)", (titleAlert, contentAlert, dateAlert))
            mysql.connection.commit()
            cursor_alerts.close()

    return redirect("/admin")
@app.route("/admin/delete_send_alert/", methods=["GET", "POST"])
def delete_send_alert():
    '''Delete alert'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    cursor_alerts = mysql.connection.cursor()
    cursor_alerts.execute("SELECT * FROM alerts")
    if len(cursor_alerts.fetchall()) == 0:
        flash("پیغامی برای حذف وجود ندارد، همچنین سرویس پیغام غیرفعال می باشد.", 'message')
    else:
        cursor_alerts.execute("DELETE FROM alerts")
        mysql.connection.commit()
        cursor_alerts.close()

    return redirect("/admin")

@app.route("/admin/admin_notify/", methods=["GET", "POST"])
def admin_notify():
    '''Admin notify'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    # Number notifications
    number_notifications = mysql.connection.cursor()
    number_notifications.execute('SELECT * FROM notifications')
    number_notifications = str(len(number_notifications.fetchall()))

    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_notifications.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, number_notifications=number_notifications, cursor_notifications_show=cursor_notifications_show.fetchall())
@app.route("/admin/admin_send_notify/", methods=["GET", "POST"])
def admin_send_notify():
    '''Admin-Send notify'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        notifyUrlIcon = request.form['notifyUrlIcon']
        notifySubject = request.form['notifySubject']
        notifyMessage = request.form['notifyMessage']
        notifyUrlLink = request.form['notifyUrlLink']

        # Date & time
        dateNotifications = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))

        # Send notify API
        try:
            config_notify(notifySubject, notifyMessage, notifyUrlIcon, notifyUrlLink)
        
            cursor_notifications = mysql.connection.cursor()
            if cursor_notifications:
                cursor_notifications.execute("INSERT INTO notifications (iconNotifications, titleNotifications, desNotifications, urlNotifications, dateNotifications) VALUES (%s,%s,%s,%s,%s)", (notifyUrlIcon, notifySubject, notifyMessage, notifyUrlLink, dateNotifications,))
                mysql.connection.commit()
                cursor_notifications.close()
        except:
            flash("ارسال نوتیفیکیشن با مشکل مواجه شده است، لطفا مجدد امتحان نمایید.")

    return redirect("/admin")
@app.route("/delete_admin_notify/<int:id>", methods=["GET", "POST"])
def delete_admin_notify(id):
    '''Delete notify'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM notifications WHERE idNotifications = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_notify')
    elif request.method == "GET":
        return redirect("/")


@app.route("/admin/admin_api/", methods=["GET", "POST"])
def admin_api():
    '''Admin api'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]

    # Show api
    cursor_api_show = mysql.connection.cursor()
    cursor_api_show.execute("SELECT * FROM api")

    # Number api
    number_api = mysql.connection.cursor()
    number_api.execute('SELECT * FROM api')
    number_api = str(len(number_api.fetchall()))

    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_api.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, number_api=number_api, cursor_api_show=cursor_api_show.fetchall())
@app.route("/delete_admin_api/<int:id>", methods=["GET", "POST"])
def delete_admin_api(id):
    '''Delete admin api'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM api WHERE idApi = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_api')
    elif request.method == "GET":
        return redirect("/")
@app.route("/accept_admin_api/<int:id>", methods=["GET", "POST"])
def accept_admin_api(id):
    '''Accept api'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('SELECT emailApi FROM api WHERE idApi = {}'.format(id))
        
        cur_username = mysql.connection.cursor()
        cur_username.execute('SELECT usernameApi FROM api WHERE idApi = {}'.format(id))

        cur_password = mysql.connection.cursor()
        cur_password.execute('SELECT passwordApi FROM api WHERE idApi = {}'.format(id))

        # Send email `Api` for User
        msg_ = Message(
            subject= 'تایید حساب و رمز عبور شما در توسعه دهندگان داها.',
            recipients= [f'{cur.fetchone()[0]}'])
        msg_.html = f"<div style='direction: rtl;'><p>توسعه دهنده عزیز {cur_username.fetchone()[0]}،</p><br><h4>حساب شما در توسعه دهندگان داها با موفقیت تایید شد، رمز عبور شما برای استفاده از APIs:</h4><div style='margin: 1rem 0;font-size: 18px;font-weight: 700;border-bottom: 1px solid #808080;'>{cur_password.fetchone()[0]}</div> <br> <h4>به جمع خانواده داها خوش آمدید، امیدواریم تجربه خوبی در پلتفرم داها داشته باشید.</h4> <br> <h3>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg_)
    
        return redirect('/admin/admin_api')
    elif request.method == "GET":
        return redirect("/")


@sitemapper.include(lastmod="2024-03-01")
@app.route("/pages/majors/", methods=["GET"])
def majors():
    '''Majors'''
    # User check session
    if session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                    
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/majors.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-03-01")
@app.route("/pages/sites/", methods=["GET"])
def sites():
    '''Sites'''
    if request.method == "POST":
        titleSites = request.form.get('titleSites')
        urlSites = request.form.get('urlSites')

        # Date & time
        dateSites = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_sites = mysql.connection.cursor()
        if cursor_sites:
            cursor_sites.execute("INSERT INTO sites (titleSites, urlSites, dateSites) VALUES (%s,%s,%s)", (titleSites, urlSites, dateSites,))
            mysql.connection.commit()
            cursor_sites.close()
    # User check session
    elif session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # Show sites
    cursor_sites_show = mysql.connection.cursor()
    cursor_sites_show.execute("SELECT * FROM sites")
    
    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                        
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/sites.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_sites_show=cursor_sites_show.fetchall(), return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-03-02")
@app.route("/pages/food-reservation/", methods=["GET"])
def food_reservation():
    '''Food reservation'''
    # User check session
    if session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                            
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/food-reservation.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-03-03")
@app.route("/pages/forums/", methods=["GET"])
def forums():
    '''Forums'''
    # User check session
    if session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                                
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/forums.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-03-06")
@app.route("/pages/technologist/", methods=["GET", "POST"])
def technologist():
    '''Technologist'''
    if request.method == "POST":
        usernameTechnologist = request.form.get('usernameTechnologist')
        titleTechnologist = request.form.get('titleTechnologist')
        titleJobTechnologist = request.form.get('titleJobTechnologist')
        emailTechnologist = request.form.get('emailTechnologist')
        phoneTechnologist = request.form.get('phoneTechnologist')
        categoryTechnologist = request.form.get('categoryTechnologist')
        addressTechnologist = request.form.get('addressTechnologist')
        desTechnologist = request.form.get('desTechnologist')
        fileTechnologist = request.files.get('fileTechnologist')
        selectExpirTechnologist = request.form.get('selectExpirTechnologist')

        # Upload & rename file
        fileTechnologist.save(fileTechnologist.filename)
        os.rename(fileTechnologist.filename, f'./static/media/uploads/{usernameTechnologist}_{titleTechnologist}.png')

        # Date & time
        dateTechnologist = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_technologist = mysql.connection.cursor()
        if cursor_technologist:
            cursor_technologist.execute("INSERT INTO technologistget (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, statusTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (f"{usernameTechnologist}_{titleTechnologist}.png", usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, selectExpirTechnologist, "درحال بررسی",))
            mysql.connection.commit()
            cursor_technologist.close()

            # Send email `Technologist` for User
            msg = Message(
                subject= 'درخواست ثبت آگهی شما برای داها ارسال شد.',
                recipients= [emailTechnologist])
            msg.html = f"<div style='direction: rtl;'><p>{usernameTechnologist} عزیز،</p><h4>درخواست شما تحت عنوان {titleTechnologist}، با موفقیت ارسال شد، و هم اکنون در حال بررسی می باشد.</h4><br><h3>مشخصات آگهی شما</h3><img src='{web_url}static/media/uploads/{usernameTechnologist}_{titleTechnologist}.png' style='width: 50px;height: 50px;border-radius: 9999px;'><p>نام و نام خانوادگی: {usernameTechnologist}</p><p>عنوان آکهی: {titleTechnologist}</p><p>نوع آگهی: {titleJobTechnologist}</p><p>ایمیل: {emailTechnologist}</p><p>شماره تماس: {phoneTechnologist}</p><p>دسته بندی: {categoryTechnologist}</p><p>آدرس محل کار: {addressTechnologist}</p><p>توضیحات: {desTechnologist}</p> <br> <p>تاریخ ثبت آگهی: {dateTechnologist}</p> <p>بسته: {selectExpirTechnologist}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)
            # Send email `Technologist` for Admin
            msg_admin = Message(
                subject= 'درخواست ثبت آگهی جدید',
                recipients= [email_admin])
            msg_admin.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>یک درخواست ثبت آگهی تحت عنوان {titleTechnologist} به داها ارسال شده است، لطفا <a href='{web_url}admin/admin_technologist/'>وارد داشبورد</a> شوید و درخواست را بررسی کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_admin)

    # User check session
    elif session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # Show technologist
    cursor_technologist_show = mysql.connection.cursor()
    cursor_technologist_show.execute("SELECT * FROM technologistset")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                                    
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/technologist.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, pricePackages=price_packages, cursor_technologist_show=cursor_technologist_show.fetchall(), return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-03-07")
@app.route("/pages/events/", methods=["GET"])
def events():
    '''Events'''
    if request.method == "POST":
        imageUrlEvents = request.form.get('imageUrlEvents')
        titleEvents = request.form.get('titleEvents')
        desEvents = request.form.get('desEvents')
        urlEvents = request.form.get('urlEvents')

        # Date & time
        dateEvents = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_events = mysql.connection.cursor()
        if cursor_events:
            cursor_events.execute("INSERT INTO events (imageUrlEvents, titleEvents, desEvents, urlEvents, dateEvents) VALUES (%s,%s,%s,%s,%s)", (imageUrlEvents, titleEvents, desEvents, urlEvents, dateEvents,))
            mysql.connection.commit()
            cursor_events.close()
    # User check session
    elif session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # Show events
    cursor_events_show = mysql.connection.cursor()
    cursor_events_show.execute("SELECT * FROM events")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                                        
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/events.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_events_show=cursor_events_show.fetchall(), return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-03-07")
@app.route("/pages/publishers/", methods=["GET"])
def publishers():
    '''Publishers'''
    if request.method == "POST":
        titleHandout = request.form.get('titleHandout')
        linkHandout = request.form.get('linkHandout')

        # Date & time
        datePublishers = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_publishers = mysql.connection.cursor()
        if cursor_publishers:
            cursor_publishers.execute("INSERT INTO publishers (titleHandout, linkHandout, datePublishers) VALUES (%s,%s,%s)", (titleHandout, linkHandout, datePublishers,))
            mysql.connection.commit()
            cursor_publishers.close()
    # User check session
    elif session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # Show publishers
    cursor_publishers_show = mysql.connection.cursor()
    cursor_publishers_show.execute("SELECT * FROM publishers")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                                            
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/publishers.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_publishers_show=cursor_publishers_show.fetchall(), return_title_ad=return_title_ad, cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-07-12")
@app.route("/pages/teachers-notifications/", methods=["GET"])
def teachers_notifications():
    '''Teachers notifications'''
    # User check session
    if session.values():
        session_user_email = session['email']
        session_user_name = session['userName']
    else:
        return redirect("/login")

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
                                                            
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT * FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show teachers notifications
    cursor_teachers_notifications_show = mysql.connection.cursor()
    cursor_teachers_notifications_show.execute("SELECT * FROM teachersnotifications")

    # Show notifications
    cursor_notifications_show = mysql.connection.cursor()
    cursor_notifications_show.execute("SELECT * FROM notifications")

    return render_template("pages/teachers-notifications.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_teachers_notifications_show=cursor_teachers_notifications_show.fetchall(), cursor_notifications_show=cursor_notifications_show.fetchall())

@sitemapper.include(lastmod="2024-05-27")
@app.route("/dl/", methods=["GET"])
def dl():
    '''Download app/Landing page'''
    return render_template("daha-landing/index.html")
@sitemapper.include(lastmod="2024-07-29")
@app.route("/api/", methods=["GET"])
def api():
    '''Api page'''
    return render_template("daha-landing/api.html")
@app.route("/api_singup/", methods=["GET", "POST"])
def api_singup():
    '''Api singup'''
    if request.method == "POST":
        usernameApi = request.form.get('usernameApi')
        emailApi = request.form.get('emailApi')
        numberApi = request.form.get('numberApi')

        # Date & time
        dateSingupApi = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        # Password random generate (10 NUM)
        passwordApi = rn.randint(1000000001, 9999999998)

        cursor = mysql.connection.cursor()
        if (emailApi) and cursor.execute("SELECT * FROM api WHERE emailApi = %s", (emailApi,)):
            flash('این ایمیل قبلا استفاده شده است.', 'error')
        else:
            flash('ثبت نام شما با موفقیت انجام شد.', 'info')
            
            cursor.execute("INSERT INTO api (usernameApi, emailApi, numberApi, passwordApi, dateSinginApi) VALUES (%s,%s,%s,%s,%s)", (usernameApi, emailApi, numberApi, passwordApi, dateSingupApi,))
            mysql.connection.commit()
            cursor.close()

            # Send email `Singup` for User
            msg = Message(
                subject= 'ثبت نام شما در توسعه دهندگان داها با موفقیت انجام شد.',
                recipients= [emailApi])
            msg.html = f"<div style='direction: rtl;'><p>توسعه دهنده عزیز {usernameApi}،</p><h4>حساب کاربری شما در توسعه دهندگان داها با موفقیت ایجاد شد، به زودی کارشناسان ما با شما تماس می گیرند و رمز عبور وب سرویس برای شما ایمیل می شود.</h4><br><h4>به جمع خانواده داها خوش آمدید، امیدواریم تجربه خوبی در پلتفرم داها داشته باشید.</h4> <br> <h3>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)
            # Send email `Singup` for Admin
            msg2 = Message(
                subject= 'ثبت نام توسعه دهنده جدید',
                recipients= [email_admin])
            msg2.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>توسعه دهنده ای با نام {usernameApi} درخواست استفاده از وب سرویس ها را دارد، لطفا <a href='{web_url}admin/admin_technologist/'>وارد داشبورد</a> شوید و با او تماس برقرار کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg2)
    
    return redirect("/api/")

@app.route("/api/users/", methods=["GET"])
@auth.login_required
def api_users():
    return APIRunning.api_users()
@app.route("/api/users_email/", methods=["GET"])
@auth.login_required
def api_users_email():
    return APIRunning.api_users_email()
@app.route("/api/ads/", methods=["GET"])
@auth.login_required
def api_ads():
    return APIRunning.api_ads()

@app.route("/update/", methods=["GET"])
def update_redirect():
    '''Update redirect'''
    return render_template("update.html")


# Run app
if (__name__ == "__main__"):
    app.run(debug=False) # For Deploy Project `True` To Change `False`
