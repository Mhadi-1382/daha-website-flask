
'''
CONNECT THE DATABASE TO PERFORM AUTOMATIC & SCHEDULER TASKS . v1.0.0
'''

from app import app, email_admin, web_url
from persiantools.jdatetime import JalaliDateTime
from flask_scheduler import Scheduler
from email.message import EmailMessage
import smtplib
import MySQLdb
import os

mysqlSCHED = MySQLdb.connect(
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_NAME', 'DahaDB')
)

sched = Scheduler(app)

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(email_admin, '')
msg = EmailMessage()
msg['From'] = email_admin


class TasksScheduler:
    '''
    Includes functions of automatic tasks.
    '''
    @sched.runner(interval=86400)
    def task_auto_delete_ad():
        current_date_str = str(JalaliDateTime.now().strftime("%Y-%m-%d"))

        cur_read_date_data = mysqlSCHED.cursor()
        cur_read_date_data.execute('SELECT dateExpirTechnologist FROM technologistset WHERE dateExpirTechnologist = "{}"'.format(current_date_str))

        try:
            if cur_read_date_data.fetchone()[0]:
                print(" * AUTO DELETE AD ... ON")

                cur_email_title = mysqlSCHED.cursor()
                cur_email_title.execute('SELECT titleTechnologist, emailTechnologist FROM technologistset WHERE dateExpirTechnologist = "{}"'.format(current_date_str))
                for email_title_auto_delete_ad in cur_email_title.fetchall():
                    msg['Subject'] = f'بسته آگهی {str(email_title_auto_delete_ad[0])} در داها  به پایان رسیده است.'
                    msg['To'] = [str(email_title_auto_delete_ad[1])]
                    msg.set_content(f"<div style='direction: rtl;'><p>{str(email_title_auto_delete_ad[1])} عزیز،</p><h4>بسته آگهی {email_title_auto_delete_ad[0]} در داها به پایان رسیده است،</h4><h4>برای تمدید مجدد میتوانید درخواست خود را دوباره ارسال و یا با پشتیبانی ارتباط برقرار کنید.</h4> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>", subtype='html')

                    server.send_message(msg)

                    cur_auto_delete_ad = mysqlSCHED.cursor()
                    cur_auto_delete_ad.execute('DELETE FROM technologistset WHERE dateExpirTechnologist = "{}" AND emailTechnologist = "{}"'.format(current_date_str, str(email_title_auto_delete_ad[1])))
                    mysqlSCHED.commit()

                    print(email_title_auto_delete_ad[0])
                    print(email_title_auto_delete_ad[1])
            else:
                cur_email_title.close()
                cur_auto_delete_ad.close()
                server.quit()
        except:
            print(" * AUTO DELETE AD ... OFF")

    # @sched.runner(interval=10)
    # def task_auto_send_email():
    #     msg['Subject'] = 'آگهی های هفتگی داها'
    #     msg.set_content(f"<div style='direction: rtl;'> <br><br><br> <h4>با تشکر، <br> <a href='{web_url}'>داها</a></h4></div>", subtype='html')

    #     select_expir_technologist = "2"

    #     cur_read_email_data = mysqlSCHED.cursor()
    #     cur_read_email_data.execute('SELECT selectExpirTechnologist FROM technologistset WHERE selectExpirTechnologist = "{}"'.format(select_expir_technologist))

    #     try:
    #         if cur_read_email_data.fetchone()[0]:
    #             print(" * AUTO SEND EMAIL ... ON")

    #             cur_email = mysqlSCHED.cursor()
    #             cur_email.execute('SELECT emailTechnologist FROM technologistset WHERE selectExpirTechnologist = "{}"'.format(select_expir_technologist))
    #             l = []
    #             l.append(cur_email.fetchall())
    #             for email_auto_send in l:
    #                 for j in email_auto_send:
    #                     msg['To'] = [str(email_auto_send[0])]

    #                     server.send_message(msg)

    #                     print(j[0])
    #         else:
    #             cur_email.close()
    #             server.quit()
    #     except:
    #         print(" * AUTO SEND EMAIL ... OFF")
