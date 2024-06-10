
'''
DAHA Application Flask
Created on date: 1402/12/02
Built on date: 1403/01/28

View source code on GitHub: https://github.com/Mhadi-1382/daha-website-flask
'''

from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_mysqldb import MySQL
from fileinput import filename
from flask_sitemapper import Sitemapper
from flask_mail import Mail, Message
from send_notify import config_notify

from datetime import *
from persiantools.jdatetime import JalaliDateTime
import os

# Version DAHA
_ver = "1.0.0"
# Website url
web_url = "https://dahauni.ir/"
# Email admin
email_admin = "info.daha.uni@gmail.com"
# Username admin
username_admin = "admin"

# Object flask app
app = Flask(__name__)

# Config DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'DahaDB'
# app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'services.irn3.chabokan.net')
# app.config['MYSQL_USER'] = os.getenv('DB_USER', 'flask514_eric')
# app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'peSaB65R4fOR')
# app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'flask514_eric')
# app.config['MYSQL_PORT'] = int(os.getenv('DB_PORT', 55063))

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=15)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.secret_key = os.urandom(24)

# Config EMAIL
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = f'{email_admin}'
app.config['MAIL_PASSWORD'] = 'iimh fvtd ijco lrae'
app.config['MAIL_DEFAULT_SENDER'] = f'{email_admin}'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Object mail
mail = Mail(app)

# Object DB (MySQL)
mysql = MySQL(app)

# Object sitemap.xml
sitemapper = Sitemapper()
sitemapper.init_app(app)


@app.errorhandler(404)
def not_found_page(e):
    '''Error 404'''
    return render_template("404.html")


@app.route("/sitemap.xml/")
def sitemap():
    '''Sitemap'''
    return sitemapper.generate()


@sitemapper.include(lastmod="1402/12/06")
@app.route("/", methods=["GET", "POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Show alert
    cursor_alerts = mysql.connection.cursor()
    cursor_alerts.execute("SELECT * FROM alerts")

    return render_template("index.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad, cursor_alerts=cursor_alerts.fetchall())


@sitemapper.include(lastmod="1402/12/08")
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

            # Send email `Singup`
            msg = Message(
                subject= 'ثبت نام شما در داها با موفقیت انجام شد.',
                recipients= [email])
            msg.html = f"<div style='direction: rtl;'><p>{username} عزیز،</p><h4>حساب کاربری شما در داها با موفقیت ایجاد شد.</h4><br><h2>مشخصات حساب کاربری</h2><p>نام کاربری: {username}</p><p>ایمیل: {email}</p><p>رمز عبور: {password}</p> <br> <h3 style='color: red;'>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)

            session['userName'] = username
            session['email'] = email
            session['password'] = password

            return redirect("/")

    return render_template("singup.html")
@sitemapper.include(lastmod="1402/12/08")
@app.route("/login/", methods=["GET", "POST"])
def login():
    '''Login'''
    if request.method == "POST":
        username = request.form['userName']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        if cursor.execute("SELECT * FROM users WHERE userName = %s AND email = %s AND password = %s", (username, email, password,)) and (username, email, password):
            session['userName'] = username
            session['email'] = email
            session['password'] = password

            if username == username_admin and email == email_admin:
                return redirect("/admin")

            cursor.fetchone()

            return redirect("/")
        else:
            flash('ورود به سیستم انجام نشد، لطفا ایمیل و رمز عبور خود را بررسی کنید.', 'error')

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

            # Send email `Forget password`
            msg = Message(
                subject= 'بازیابی رمز عبور در داها با موفقیت انجام شد.',
                recipients= [email])
            msg.html = f"<div style='direction: rtl;'><p>کاربر عزیز</p><h4>بازیابی رمز عبور با موفقیت انجام شده است.</h4> <br> <div style='text-align: center;padding: 1rem;background-color: rgb(233, 233, 233);border-radius: 10px;'>{return_password}</div> <br> <h3 style='color: red;'>تذکر: از در اختیار قرار دادن این اطلاعات به دیگران خودداری نمایید، زیرا این اطلاعات مختص شماست.</h3> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)

            return redirect("/login")
        else:
            flash('کاربر عزیز، کاربری با این ایمیل یافت نشد.', 'error')

    return render_template("user/forget_password.html")
@app.route("/user/edit_info/", methods=["GET","POST","UPDATE"])
def edit_info():
    '''Edit info'''
    if request.method == "POST":
        username = request.form['userName']
        password = request.form['password']

        # Date & time
        dateSingup = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))

        cursor = mysql.connection.cursor()
        if (username) and cursor.execute("SELECT * FROM users WHERE userName = %s", (username,)):
            flash("این نام کاربری قبلا استفاده شده است.", 'error')

            return redirect("/")
        elif session['email'] and cursor.execute("SELECT * FROM users WHERE email = %s", (session['email'],)):
            cursor.execute(f"UPDATE users SET userName = '{username}', password = '{password}', dateSingin = '{dateSingup}' WHERE email = '{session['email']}'")
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
@app.route("/user/delete_account/", methods=["GET","POST","DELETE"])
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
            subject= "حذف حساب کاربری در داها",
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


@app.route("/admin/", methods=["GET","POST"])
def admin():
    '''Admin-Dashbord'''
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

    # Number users
    cursor_user = mysql.connection.cursor()
    cursor_user.execute('SELECT * FROM users')
    number_users = str(len(cursor_user.fetchall()))
    # Number comments
    cursor_comment = mysql.connection.cursor()
    cursor_comment.execute('SELECT * FROM comment')
    number_comments = str(len(cursor_comment.fetchall()))
    # Number technologists
    cursor_technologist = mysql.connection.cursor()
    cursor_technologist.execute('SELECT * FROM technologistget')
    number_technologists = str(len(cursor_technologist.fetchall()))
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    # Auto delete ad
    # Date & time
    datetime = str(JalaliDateTime.now().strftime("%Y-%m-%d"))

    cur_auto_delete_ad = mysql.connection.cursor()
    cur_auto_delete_ad.execute(f'SELECT dateExpir FROM technologistset WHERE dateExpir = "{datetime}"')
    auto_delete_ad_record = cur_auto_delete_ad.fetchone()

    cur_email_technologist = mysql.connection.cursor()
    cur_email_technologist.execute(f'SELECT emailTechnologist FROM technologistset WHERE dateExpir = "{datetime}"')
    email_technologist = cur_email_technologist.fetchall()
    if auto_delete_ad_record and datetime:
        auto_delete_ad = mysql.connection.cursor()

        # Send email for user
        for email_ in email_technologist:
            msg = Message(
                subject= 'انقضای آگهی شما در داها به پایان رسیده است',
                recipients= [str(email_[0])])
            msg.html = f"<div style='direction: rtl;'><p>{str(email_[0])} عزیز،</p><h4>انقضای آگهی شما در داها به پایان رسیده است،</h4><h4>برای تمدید مجدد میتوانید درخواست خود را دوباره ارسال و یا با پشتیبانی ارتباط برقرار کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)

            auto_delete_ad.execute(f'DELETE FROM technologistset WHERE dateExpir = "{datetime}"')
            mysql.connection.commit()
        auto_delete_ad.close()

    return render_template("admin.html", _ver=_ver, email_admin=email_admin, number_users=number_users, number_comments=number_comments, users=cursor_user_show.fetchall(), comments=cursor_comment_show.fetchall(), session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_technologist_show=cursor_technologist_show.fetchall(), number_technologists=number_technologists, cursor_events_show=cursor_events_show.fetchall(), number_events=number_events, cursor_sites_show=cursor_sites_show.fetchall(), number_sites=number_sites, cursor_publishers_show=cursor_publishers_show.fetchall(), number_publishers=number_publishers, cursor_ticket_show=cursor_ticket_show.fetchall(), number_ticket=number_ticket, show_email_users=show_email_users, return_title_ad=return_title_ad)

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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_comments.html", _ver=_ver, email_admin=email_admin, comments=cursor_comment_show.fetchall(), session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, number_comments=number_comments, return_title_ad=return_title_ad)
@app.route("/delete_comments/<int:id>", methods=["GET","POST","DELETE"])
def delete_comments(id):
    '''Delete comments'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM comment WHERE idComment = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_comments')
@app.route("/comment/", methods=["GET","POST"])
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
                subject= 'ثبت نظر در داها',
                recipients= [email_admin])
            msg_admin.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>کاربر {username}، یک نظر ارسال کردند.</h4><h4>متن پیام</h4><p>{message}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_admin)
        
            return redirect("/")

        else:
            flash("ارسال پیام شما با مشکل مواجه شده است، لطفا ورودی را بررسی کنید.", 'error')

    return redirect("/")

@app.route("/admin/admin_users/")
def admin_users():
    '''Admin Users'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")
        
    cursor_user_show = mysql.connection.cursor()
    cursor_user_show.execute('SELECT * FROM users')

    # Number users
    cursor_user = mysql.connection.cursor()
    cursor_user.execute('SELECT * FROM users')
    number_users = str(len(cursor_user.fetchall()))

    # User avatar
    session_user_email = session['email']
    session_user_name = session['userName']
    session_user_name_filter = session['userName'][0]
            
    # Check status ad
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT titleTechnologist FROM technologistget")
    if len(cursor.fetchall()) >= 0:
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_users.html", _ver=_ver, email_admin=email_admin, users=cursor_user_show.fetchall(), session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, number_users=number_users, return_title_ad=return_title_ad)
@app.route("/delete_users/<int:id>", methods=["GET","POST","DELETE"])
def delete_users(id):
    '''Delete users'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM users WHERE id = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_users')

@app.route("/admin/admin_files/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_files.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, path_folder_files_uploaded=path_folder_files_uploaded, number_files=number_files, return_title_ad=return_title_ad)
@app.route("/delete_admin_files/<file>", methods=["GET","POST","DELETE"])
def delete_admin_files(file):
    '''Delete files'''
    if request.method == "POST":
        os.remove("static/media/uploads/{}".format(file))
    
        return redirect('/admin/admin_files')
@app.route("/upload_file/", methods=["GET","POST"])
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
    
    return render_template("admin.html")

@app.route("/admin/admin_technologist/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_technologist.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_technologist_show=cursor_technologist_show.fetchall(), cursor_technologist_set_show=cursor_technologist_set_show.fetchall(), number_technologists=number_technologists, number_technologists_set=number_technologists_set, return_title_ad=return_title_ad)
@app.route("/pages/technologist_set/", methods=["GET","POST"])
def technologist_set():
    '''Technologist set'''
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
        dateExpir = request.form.get('dateExpir')

        # Date & time
        dateTechnologist = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_technologist = mysql.connection.cursor()
        if cursor_technologist:
            cursor_technologist.execute("INSERT INTO technologistset (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, dateExpir) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (fileUrlTechnologist, usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist, dateExpir,))
            mysql.connection.commit()
            cursor_technologist.close()

            # Send email `Technologist set`
            msg = Message(
                subject= 'آگهی شما با موفقیت در داها تایید شد.',
                recipients= [emailTechnologist])
            msg.html = f"<div style='direction: rtl;'><p>{usernameTechnologist} عزیز تبریک،</p><h4>درخواست شما برای ثبت آگهی در داها بررسی و در بخش فن آور اضافه شده است.</h4><br><h2>مشخصات آگهی شما</h2><img src='{fileUrlTechnologist}' alt='{fileUrlTechnologist}'><p>نام و نام خانوادگی: {usernameTechnologist}</p><p>عنوان شغل: {titleTechnologist}</p><p>عنوان آگهی: {titleJobTechnologist}</p><p>ایمیل: {emailTechnologist}</p><p>شماره تماس: {phoneTechnologist}</p><p>دسته بندی: {categoryTechnologist}</p><p>آدرس محل کار: {addressTechnologist}</p><p>توضیحات: {desTechnologist}</p> <br> <p>تاریخ ثبت درخواست {dateTechnologist}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)

        return redirect("/pages/technologist")
    
    return render_template("pages/technologist.html")
@app.route("/delete_technologists_set_ad/<int:id>", methods=["GET","POST","DELETE"])
def delete_technologists_set_ad(id):
    '''Delete technologists set ad'''
    if request.method == "POST":
        # Send email `Delete technologists set ad`
        cur_email_user = mysql.connection.cursor()
        cur_email_user.execute('SELECT emailTechnologist FROM technologistset WHERE idTechnologist = {}'.format(id))
        emailTechnologist = cur_email_user.fetchone()
        
        msg = Message(
            subject= 'انقضای آگهی شما در داها به پایان رسیده است',
            recipients= [str(emailTechnologist[0])])
        msg.html = f"<div style='direction: rtl;'><p>{str(emailTechnologist[0])} عزیز،</p><h4>انقضای آگهی شما در داها به پایان رسیده است،</h4><h4>برای تمدید مجدد میتوانید درخواست خود را دوباره ارسال و یا با پشتیبانی ارتباط برقرار کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistset WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')
@app.route("/delete_technologists_get_ad/<int:id>", methods=["GET","POST","DELETE"])
def delete_technologists_get_ad(id):
    '''Delete technologists get ad'''
    if request.method == "POST":
        # Send email `Delete technologists get ad`
        cur_email_user = mysql.connection.cursor()
        cur_email_user.execute('SELECT emailTechnologist FROM technologistget WHERE idTechnologist = {}'.format(id))
        emailTechnologist = cur_email_user.fetchone()
        
        msg = Message(
            subject= 'آگهی شما در داها تایید نشده است',
            recipients= [str(emailTechnologist[0])])
        msg.html = f"<div style='direction: rtl;'><p>{str(emailTechnologist[0])} عزیز متاسفانه،</p><h4>درخواست شما برای ثبت آگهی رد شده است،</h4><h4>در صورت نیاز کارشناسان ما با شما تماس خواهند گرفت.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
        mail.send(msg)

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistget WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')
@app.route("/delete_technologists_get/<int:id>", methods=["GET","POST","DELETE"])
def delete_technologists_get(id):
    '''Delete technologists get'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistget WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')
@app.route("/delete_technologists_set/<int:id>", methods=["GET","POST","DELETE"])
def delete_technologists_set(id):
    '''Delete technologists set'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM technologistset WHERE idTechnologist = {}'.format(id))
        mysql.connection.commit()
        cur.close()
    
        return redirect('/admin/admin_technologist')

@app.route("/admin/admin_events/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_events.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_events_show=cursor_events_show.fetchall(), number_events=number_events, return_title_ad=return_title_ad)
@app.route("/delete_events/<int:id>", methods=["GET","POST","DELETE"])
def delete_events(id):
    '''Delete events'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM events WHERE idEvents = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_events')

@app.route("/admin/admin_sites/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_sites.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_sites_show=cursor_sites_show.fetchall(), number_sites=number_sites, return_title_ad=return_title_ad)
@app.route("/delete_sites/<int:id>", methods=["GET","POST","DELETE"])
def delete_sites(id):
    '''Delete sites'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM sites WHERE idSites = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_sites')

@app.route("/admin/admin_publishers/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("admin/admin_publishers.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_publishers_show=cursor_publishers_show.fetchall(), number_publishers=number_publishers, return_title_ad=return_title_ad)
@app.route("/delete_publisher/<int:id>", methods=["GET","POST","DELETE"])
def delete_publisher(id):
    '''Delete publisher'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM publishers WHERE idPublishers = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_publishers')

@app.route("/admin/admin_ticket/", methods=["GET","POST"])
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

    return render_template("admin/admin_ticket.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_ticket_show=cursor_ticket_show.fetchall(), number_ticket=number_ticket)
@app.route("/delete_ticket/<int:id>", methods=["GET","POST","DELETE"])
def delete_ticket(id):
    '''Delete ticket'''
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM ticket WHERE idTicket = {}'.format(id))
        mysql.connection.commit()
    
        return redirect('/admin/admin_ticket')
@app.route("/ticket/", methods=["GET","POST"])
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

            # Send email `Ticket` for Admin
            msg_admin = Message(
                subject= 'ثبت تیکت در داها',
                recipients= [email_admin])
            msg_admin.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>کاربر {usernameTicket}، یک تیکت ارسال کردند.</h4><h4>عنوان تیکت: {titleTicket}</h4><h4>متن تیکت: </h4><p>{messageTicket}</p> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg_admin)
        
            return redirect("/")

        else:
            flash("ارسال تیکت شما با مشکل مواجه شده است، لطفا ورودی را بررسی کنید.", 'error')

    return redirect("/")


@app.route("/admin/admin_send_email/", methods=["GET","POST"])
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

@app.route("/admin/admin_send_alert/", methods=["GET","POST"])
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
@app.route("/admin/delete_send_alert/", methods=["GET","POST"])
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

@app.route("/admin/admin_send_notify/", methods=["GET","POST"])
def admin_send_notify():
    '''Admin-Send notify'''
    if session['userName'] != username_admin and session['email'] != email_admin:
        return redirect("/404")

    if request.method == "POST":
        notifySubject = request.form['notifySubject']
        notifyMessage = request.form['notifyMessage']
        notifyUrlImage = request.form['notifyUrlImage']

        # Send notify API
        try:
            config_notify(notifySubject, notifyMessage, notifyUrlImage)
        except:
            flash("ارسال نوتیفیکیشن با مشکل مواجه شده است، لطفا مجدد امتحان نمایید.")

    return redirect("/admin")


@sitemapper.include(lastmod="1402/12/11")
@app.route("/pages/majors/")
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("pages/majors.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad)

@sitemapper.include(lastmod="1402/12/11")
@app.route("/pages/sites/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("pages/sites.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_sites_show=cursor_sites_show.fetchall(), return_title_ad=return_title_ad)

@sitemapper.include(lastmod="1402/12/12")
@app.route("/pages/food-reservation/")
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("pages/food-reservation.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad)

@sitemapper.include(lastmod="1402/12/13")
@app.route("/pages/forums/")
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("pages/forums.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, return_title_ad=return_title_ad)

@sitemapper.include(lastmod="1402/12/16")
@app.route("/pages/technologist/", methods=["GET","POST"])
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

        # Upload & rename file
        fileTechnologist.save(fileTechnologist.filename)
        os.rename(fileTechnologist.filename, f'./static/media/uploads/{usernameTechnologist}_{titleTechnologist}.png')

        # Date & time
        dateTechnologist = str(JalaliDateTime.now().strftime("%Y-%m-%d %H:%M"))
        
        cursor_technologist = mysql.connection.cursor()
        if cursor_technologist:
            cursor_technologist.execute("INSERT INTO technologistget (usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (usernameTechnologist, titleTechnologist, titleJobTechnologist, emailTechnologist, phoneTechnologist, categoryTechnologist, addressTechnologist, desTechnologist, dateTechnologist,))
            mysql.connection.commit()
            cursor_technologist.close()

            # Send email `Technologist`
            msg = Message(
                subject= 'درخواست شما در داها ارسال شد.',
                recipients= [emailTechnologist])
            msg.html = f"<div style='direction: rtl;'><p>{usernameTechnologist} عزیز،</p><h4>در خواست شما با عنوان {titleTechnologist}، با موفقیت ارسال شد، و هم اکنون در حال بررسی و تایید است.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
            mail.send(msg)
            # Send email `Technologist` for Admin
            msg_admin = Message(
                subject= 'درخواست ثبت آگهی',
                recipients= [email_admin])
            msg_admin.html = f"<div style='direction: rtl;'><p>مدیر عزیز سلام،</p><h4>یک درخواست ثبت آگهی با عنوان {titleTechnologist} به داها ارسال شده است، لطفا وارد داشبورد شوید و درخواست را بررسی کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>"
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("pages/technologist.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_technologist_show=cursor_technologist_show.fetchall(), return_title_ad=return_title_ad)

@sitemapper.include(lastmod="1402/12/17")
@app.route("/pages/events/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("pages/events.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_events_show=cursor_events_show.fetchall(), return_title_ad=return_title_ad)

@sitemapper.include(lastmod="1402/12/17")
@app.route("/pages/publishers/", methods=["GET","POST"])
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
        cursor.execute("SELECT titleTechnologist FROM technologistget WHERE usernameTechnologist = %s AND emailTechnologist = %s", (session['userName'], session['email'],))
        return_title_ad = cursor.fetchall()

    return render_template("pages/publishers.html", _ver=_ver, email_admin=email_admin, session_user_email=session_user_email, session_user_name=session_user_name, session_user_name_filter=session_user_name_filter, cursor_publishers_show=cursor_publishers_show.fetchall(), return_title_ad=return_title_ad)


@sitemapper.include(lastmod="1403/03/16")
@app.route("/download/", methods=["GET","POST"])
def download():
    '''Download app/Landing page'''
    return render_template("")

# Run app
if (__name__ == "__main__"):
    app.run(debug=True) # For Deploy Project `True` To Change `False`
