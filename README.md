# Pynetwork

Designed to run as Linux crontab job on Raspberry Pi, for network ping/upload/download speed mesurements and analysis.

##  Examples
```
netcheck.py -u 2 -d 25 -p 4
netcheck.py -u 4
```

### Optional arguments

```
-h, --help  show this help message and exit
-d D        Download speed constraint
-u U        Upload speed constraint
-p P        Ping speed constraint
```

### Possible Configurations (can be found in netcheck/models.py file):
```
#Sets whether use real time network check (mainly used for DEBUG purposes)
self.__real_network_check
#Sets whether writing local file with the mail html content
self.__write_to_local_html_file
#Sets whether send a mail when network check is completed"""
self.__send_mail
#Sets for attaching chart html to mail
self.__attach_mail_chart
```
## Sending Mail (only Gmail SMTP implemented):

If you want to receive email you'll need to provide 3 settings in ./netcheck/models.py GlobalConfig class:

```	
RECEIVER_GMAIL_ACCOUNT = <receiver gmail account>
DEVICE_GMAIL_ACCOUNT = <sender gmail account>
DEVICE_GMAIL_PASSWORD = <sender gmail password>
```

##Data Files:

netcheck.py generates data files as its output. So you can browse history of your network performance.
* Daily charts can be found under : ./data/<date>chart.html
```
Data files hierarchy:
	./data
		/<date directory>
        	/<date>_data.json    (global data file: contains all of the information)
            /<date>_uploads.csv  (pure csv file: only uploads mesurements)
            /<date>_downlads.csv (pure csv file: only downloads mesurements)
```

## Dependencies
```
pip install pyspeedtest
pip install mail
pip install requests
```
