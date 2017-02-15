"""Script for generating html chart file (./html directory) based on local data files"""

import json
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
        """Generates chart based on given data, and outputs html file with the result
            Returns:
                path to the chart
        """
        json_path = analytics.get_jsondata_file_path(time_stamp, self.__config)
        json_content = fsutil.read_json_from_file(json_path)

        html = self.__generate_html(json.dumps(json_content))
        return self.__write_html_chart(html, time_stamp)

    def __write_html_chart(self, content, time_stamp):
        fsutil.recheck__dir(self.__config.CHART_HTML_DIR)
        path = get_daily_chart_path(self.__config, time_stamp)
        fsutil.write_to_file(path, content)
        return path


    def __generate_html(self, json_array):

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
                var data = """+ json_array + """;
                
                var ctx = document.getElementById('myChart').getContext('2d');
                uploadData = data.map(function(x){ return x.upload});
				downloadData = data.map(function(x){ return x.download});
                pingData = data.map(function(x){ return x.ping});

				labels = data.map(function(x) { 
                    return new Date((new Date(0)).setUTCSeconds(x.utcEpoch)).toLocaleTimeString()
                });

                upload_data_set = {label: 'upload', data: uploadData, backgroundColor: "rgba(0, 122, 204, 0.4)"};
                download_data_set = {label: 'download', data: downloadData, backgroundColor: "rgba(0, 153, 51, 0.4)"};
                ping_data_set = {label: 'ping', data: pingData, backgroundColor: "rgba(83, 83, 198, 0.4)"};
                new Chart(ctx, {
                    type: 'line',
                        data: {
                        labels: labels,
                        datasets: [upload_data_set , download_data_set, ping_data_set]
                    }
                });
            </script>
        </body>	
        </html>
        """
        return html_str
