"""Script for generating html chart file (./html directory) based on local data files"""

import json
import fsutil
import timeutil
import wkhtmltoimage
from jinja2 import Environment


def get_daily_chart_path(config, time):
    """Returns full path of chart, by given time """
    time_str = timeutil.format_to_date_str(time)
    path = config.CHART_HTML_DIR + time_str + config.CHART_HTML_POSTFIX
    return path

def get_daily_chart_image_path(config, time):
    """Returns full path of chart image, by given time """
    time_str = timeutil.format_to_date_str(time)
    path = config.CHART_IMG_DIR + time_str + config.CHART_IMG_POSTFIX
    return path


class ChartGenerator(object):
    """Generated html chars using Chart.js lib"""

    CHART_TEMPLATE_PATH = None

    def __init__(self, config):
        self.__config = config
        self.CHART_TEMPLATE_PATH = config.PROJ_PATH + "/templates/html_templates/chart_template.html"
        self.__env = Environment(line_statement_prefix='%',
                                 variable_start_string="${",
                                 variable_end_string="}")

    def generate_chart_image(self, time_stamp):
        """
            Generates chart image from html chart file

            Returns:
                path to the image file
        """
        fsutil.recheck_dir(self.__config.CHART_IMG_DIR)
        img_chart_path = get_daily_chart_image_path(self.__config, time_stamp)
        chart_path = get_daily_chart_path(self.__config, time_stamp)
        wkhtmltoimage.convert_html_to_image(chart_path, img_chart_path)

        return img_chart_path

    def generate_chart(self, time_stamp):
        """
            Generates chart based on given data, and outputs html file with the result
            Returns:
                path to the html file
        """
        json_path = fsutil.get_jsondata_file_path(time_stamp, self.__config)
        json_content = fsutil.read_json_from_file(json_path)

        html = self.__generate_html(json.dumps(json_content))
        return self.__write_html_chart(html, time_stamp)

    def __write_html_chart(self, content, time_stamp):
        fsutil.recheck_dir(self.__config.CHART_HTML_DIR)
        path = get_daily_chart_path(self.__config, time_stamp)
        fsutil.write_to_file(path, content)
        return path

    def __generate_html(self, json_array):
        tmpl = self.__env.from_string(fsutil.get_file_content(self.CHART_TEMPLATE_PATH))
        return tmpl.render(json_arr=json_array)

