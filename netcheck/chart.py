"""Script for generating html chart file (./html directory) based on local data files"""

import fsutil
import timeutil
import analytics

def get_daily_chart_path(config, time):
    """Returns full path of todays' chart """
    time_str = timeutil.format_to_date_str(time)
    path = config.CHART_HTML_DIR + time_str + config.CHART_HTML_POSTFIX
    return path

class ChartGenerator:
    """Generated html chars using Chart.js lib"""
    def __init__(self, config):
        self.__config = config

    def generate_chart(self, time_stamp):
        """Generates chart based on given data, and outputs html file with the result"""
        downloads_data_file = analytics.get_downloads_csv_data(time_stamp, self.__config)
        uploads_data_file = analytics.get_uploads_csv_data(time_stamp, self.__config)

        html = self.__generate_html("["+downloads_data_file+"]", "["+uploads_data_file+"]")
        self.__write_html_chart(html, time_stamp)

    def __write_html_chart(self, content, time_stamp):
        fsutil.recheck__dir(self.__config.CHART_HTML_DIR)
        path = get_daily_chart_path(self.__config, time_stamp)
        fsutil.write_to_file(path, content)


    def __generate_html(self, uploads_arr, downloads_arr):

        html_str = """
        <!DOCTYPE html>
        <meta charset="utf-8"/>
        <html lang="en">
            <head>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.4/Chart.min.js"></script>	
            </head>
        <body>
            <canvas id="myChart"></canvas>
            <script>
                var downloadData = """+ downloads_arr+ """
                var uploadData = """ + uploads_arr+"""
                var ctx = document.getElementById('myChart').getContext('2d');
                labels =  ['00:00', '01:00', '02:00','03:00', '04:00', '05:00',
                            '06:00', '07:00', '08:00','09:00', '10:00', '11:00',
                            '12:00', '13:00', '14:00','15:00', '16:00', '17:00',
                            '18:00', '19:00', '20:00','21:00', '22:00', '23:00'];

                upload_data_set = {label: 'upload', data: downloadData, backgroundColor: "rgba(255,153,0,0.4)"};
                download_data_set = {label: 'download', data: uploadData, backgroundColor: "rgba(255,153,0,0.4)"};
                new Chart(ctx, {
                    type: 'line',
                        data: {
                        labels: labels,
                        datasets: [upload_data_set , download_data_set ]
                    }
                });
            </script>
        </body>	
        </html>
        """
        return html_str
