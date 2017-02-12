"""Script for generating mail content and sending emails to gmail accounts"""

import smtplib
import chart
import time
import fsutil
import timeutil
from requests import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

class EmailSender:
    """Responsible for emails sending"""

    SUBJECT_EMAIL = "Here is your network check update."
    GMAIL_SMTP = 'smtp.gmail.com:587'

    def send_gmail(self, message_content):
        """Sends gmail to specified account"""

        print("sending email to: "  + self.__config.get_receiver_gmail_account)
        server = smtplib.SMTP(self.GMAIL_SMTP)
        server.ehlo()
        server.starttls()

        # Record the MIME types of both parts - text/plain and text/html.
        sender = self.__config.get_agent_gmail_account
        receiver = self.__config.get_receiver_gmail_account

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.SUBJECT_EMAIL
        msg['From'] = sender
        msg['To'] = receiver

        filename = chart.get_daily_chart_path(self.__config, timeutil.utc_now())
        if self.__config.get_attach_mail_chart and fsutil.file_exist(filename):
            self.__attach_chart(filename, msg)

        # Attach parts into message container.
        msg.attach(MIMEText(message_content, 'html'))
        if server.login(sender, self.__config.get_agent_gmail_password):
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()
        else:
            print("could not login :(")

    def __attach_chart(self, filename, msg):
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    def __init__(self, config):
        self.__config = config



class MessageFormatter:
    """Formats email content"""

    OK_CSS_CLASS = "ok"
    NOT_OK_CSS_CLASS = "not-ok"

    def __init__(self, config):
        self.__config = config

    def format_message(self, result):
        """Formats message as html"""
        html = self.__create_html(result)

        if self.__config.get_write_html_file:
            self.__write_to_file(html)

        return html

    def __speed_check_title_html(self, result):

        if self.__config.get_downlad_constraint != self.__config.UNSET_CONSTRAINT:
            download_check = result.get_download_speed < self.__config.get_downlad_constraint
        else:
            download_check = False

        if self.__config.get_upload_constraint != self.__config.UNSET_CONSTRAINT:
            upload_check = result.get_upload_speed < self.__config.get_upload_constraint
        else:
            upload_check = False

        if self.__config.get_ping_constraint != self.__config.UNSET_CONSTRAINT:
            ping_check = result.get_ping_speed < self.__config.get_ping_constraint
        else:
            ping_check = False

        title = 'Network'
        ok_status = False

        if download_check or upload_check or ping_check:
            multiple = False

            if download_check:
                title = title + " download"
                multiple = True

            if upload_check:
                if multiple:
                    title = title + ", "
                title = title + " upload"
                multiple = True

            if ping_check:
                if multiple:
                    title = title + ", "
                title = title + " ping"
                multiple = True

            if multiple:
                title = title + " issues"
            else:
                title = title + " issue"
        else:
            title = title + ' speed is OK'
            ok_status = True

        return {'content': title, 'status':  ok_status}

    def __get_css(self):
        """Reads css from MAIN_CSS_PATH file"""
        try:
            with open(self.__config.MAIN_CSS_PATH, 'r') as content_file:
                content = content_file.read()
            return content
        except IOError:
            print("FileNotFound, path: " + self.__config.MAIN_CSS_PATH)

    def __write_to_file(self, html):
        try:
            with open(self.__config.OUTPUT_HTML_FILE, 'w+') as out_file:
                out_file.write(html)
        except IOError:
            print("FileNotFound, path: " + self.__config.OUTPUT_HTML_FILE)

    def __create_html(self, result):
        title = self.__speed_check_title_html(result)

        css = self.__get_css()
        time_stamp = timeutil.format_to_time_str(result.get_time_stamp)

        body_css_class = ""

        if title["status"]:
            body_css_class = self.OK_CSS_CLASS
        else:
            body_css_class = self.NOT_OK_CSS_CLASS

        #ip_addr = get('https://api.ipify.org').text

        print("download constraint: " + str(self.__config.get_downlad_constraint))
        print("upload constraint: " + str(self.__config.get_upload_constraint))
        print("ping constraint: " + str(self.__config.get_ping_constraint))

        return  """
        <html>
        <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.4/Chart.min.js"></script>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <style type="text/css" media="screen">"""+css+"""</style>
        </head>
        <body class='""" + body_css_class + """'>
            <h1>""" + title["content"] + """</h1>
            <div class="date">""" + time_stamp + """<div/>
            <div class="table">
                <h2 class="title">Results</h2>
                <span class="row">Ping : """+str(result.get_ping_speed)+""" ms</span>
                <span class="row">Upload speed : """+str(result.get_upload_speed)+""" mbps</span>
                <span class="row">Download speed : """+str(result.get_download_speed) +""" mbps</span>
            </div>
            <div class="table">
                <h2 class="title">Constraints</h2>
                <span class="row">upload-constraint: """+str(self.__config.get_upload_constraint)+ """</span>
            <span class="row">download-constraint: """+str(self.__config.get_downlad_constraint)+"""</span>
                <span class="row">ping-constraint: """+str(self.__config.get_ping_constraint)+"""</span>
            </div>
        </body>
        </html>
        """

