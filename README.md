# Pynetwork

Designed to run as Linux crontab job on Raspberry Pi, for network ping/upload/download speed measurements and analysis.


## Usage

In a terminal:

```
$ pynetwork.py -u 2 -d 25 -p 4
```

```
$ pynetwork.py -h

	usage: pynetwork.py [OPTION]...

	Network upload, download, ping speed check and notifications script

	optional arguments:
	-h, --help  show this help message and exit
	-d D        Download speed constraint
	-u U        Upload speed constraint
	-p P        Ping speed constraint
```

### Possible Configurations (can be found in config.json file):

```
{
    	//weather configurations
    	"weather":{
		//Sets whether to include weather report 
        	"takeWeatherSamples" : true,
		//Sets city code for current city
        	"openWeatherAPICityCode" : 293397 
    	},
	"gdrive" :{
        	//Sets whether upload daily json data file to Google Drive
		"uploadDailyData" : true,
		//Sets whether upload daily generated chart to Google Drive
        	"uploadDailyChart" : true
    	},
	"mail" :{
       		//Sets whether send a mail when network check is completed"""
		"sendMail": true,
		//Sets for attaching chart html to mail
		"attachMailChart" : true
 	},
    	//Sets whether use real time network check (mainly used for DEBUG purposes)
	"realNetworkCheck" : true,
    	//Sets whether writing local file with the mail html content
    	"writeLocalHtml" : true,
    	//Enables/Disables slack bot
    	"slackBotEnabled" : true
    	//Slack config
    	"slack" : {
            "enabled" : true,
            "channel" : "#network-updates"
        }
}

```

### Sending mail (Gmail only)
If you want to send mail you'll need to provide the following environment variables (separated by semi columns):

```
PYNETWORK_GMAIL_CREDENTIALS = receiver-gail-account;agent-gmail-account;agent-gmail-password
```

### Slack bot
If you want to receive slack bot updates in your slack channel, you will need to set the following environment variable:

```
SLACK_PYNETWORK_API_TOKEN  
```

## chart screenshot
![screenshot](chart_screenshot.png)

### Uploading collected data to Google Drive

If you want to upload generated files to Google drive, 
you'll need to provide ./secrets/client.secret.json file (can be downloaded from your Google API Console)


## Data Files:

pynetwork generates data files as its output. So you can browse history of your network performance.
* Daily charts can be found under : ./html/[date]_chart.html
```
Data files hierarchy:
	./data
		/<date directory>
        		/<date>_data.json    (global data file: contains all of the information)
```

## Dependencies

```
pip install mail
pip install requests
pip install --upgrade google-api-python-client
pip install httplib2
pip install jinja2
pip install slackclient
```
