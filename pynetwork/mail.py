"""Script for generating mail content and sending emails to gmail accounts"""

import smtplib
import chart
import time
import fsutil
import timeutil
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from jinja2 import Environment

class EmailSender(object):
    """Responsible for emails sending"""

    SUBJECT_EMAIL = "Here is your network check update."
    GMAIL_SMTP = 'smtp.gmail.com:587'

    def send_gmail(self, message_content):
        """Sends gmail to specified account"""
        receiver = self.__config.get_receiver_gmail_account

        logging.getLogger("PYNETWORK").info("sending email to: " + receiver)

        server = smtplib.SMTP(self.GMAIL_SMTP)
        server.ehlo()
        server.starttls()

        # Record the MIME types of both parts - text/plain and text/html.
        sender = self.__config.get_agent_gmail_account

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
            logging.getLogger("PYNETWORK").error("could not login :(")

    def __attach_chart(self, filename, msg):
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)

    def __init__(self, config):
        self.__config = config



class MessageFormatter(object):
    """Formats email content"""

    OK_CSS_CLASS = "ok"
    NOT_OK_CSS_CLASS = "not-ok"

    def __init__(self, config):
        self.__config = config
        self.MAIL_TEMPLATE_PATH = config.PROJ_PATH + "/templates/html_templates/mail_template.html"
        self.__env = Environment(line_statement_prefix='%',
                                 variable_start_string="${",
                                 variable_end_string="}")

    def format_message(self, result):
        """Formats message as html"""
        html = self.__create_html(result)

        if self.__config.get_write_html_file:
            fsutil.write_to_file(self.__config.OUTPUT_HTML_FILE, html)

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

    def __create_html(self, result):
        title = self.__speed_check_title_html(result)

        #public_ip_addr = get('https://api.ipify.org').text
        bcss_class = self.OK_CSS_CLASS if title["status"] else self.NOT_OK_CSS_CLASS

        html_template = fsutil.get_file_content(self.MAIL_TEMPLATE_PATH)
        tmpl = self.__env.from_string(html_template)

        return tmpl.render(css=fsutil.get_file_content(self.__config.MAIN_CSS_PATH),
                           title=title["content"],
                           body_css_class=bcss_class,
                           ping_speed=str(result.get_ping_speed),
                           upload_speed=str(result.get_upload_speed),
                           download_speed=str(result.get_download_speed),
                           upload_constraint=str(self.__config.get_upload_constraint),
                           download_constraint=str(self.__config.get_downlad_constraint),
                           ping_constraint=str(self.__config.get_ping_constraint),
                           time_stamp=timeutil.format_to_time_str(result.get_time_stamp))



