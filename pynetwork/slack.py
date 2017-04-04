import os
import fsutil
from jinja2 import Environment
from slackclient import SlackClient

class SlackPyNetworkBot(object):
    """Uses slack API to send messages in the defined channel as a bot user"""
    SLACK_PYNETWORK_API_TOKEN_ENV_KEY = "SLACK_PYNETWORK_API_TOKEN"
    DEFAULT_CHANNEL = "#network-updates"
    MESSAGE_TEMPLATE_PATH = None
    MESSAGE_TEMPLATE_RELATIVE_PATH = "/plain_text_templates/slack_speed_test_msg_template.txt"

    def __init__(self, config):
        self.MESSAGE_TEMPLATE_PATH = config.PROJ_PATH + self.MESSAGE_TEMPLATE_RELATIVE_PATH
        slack_token = os.environ[self.SLACK_PYNETWORK_API_TOKEN_ENV_KEY]
        self.__slack_client = SlackClient(slack_token)
        self.__env = Environment(line_statement_prefix='%',
                                 variable_start_string="${",
                                 variable_end_string="}")

    def send_message(self, message, channel_name):
        """Sends text message to slack channel"""
        self.__slack_client.api_call("chat.postMessage", channel=channel_name, text=message)

    def compose_speed_result_message(self, speed_result):
        """Composes slack message content for speed test result data"""
        plain_template = fsutil.get_file_content(self.MESSAGE_TEMPLATE_PATH)
        tmpl = self.__env.from_string(plain_template)

        result = tmpl.render(ping_result=speed_result.get_ping_speed,
                             upload_result=speed_result.get_upload_speed,
                             download_result=speed_result.get_download_speed)
        return result