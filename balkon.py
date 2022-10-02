import requests
import hashlib
import xml.etree.ElementTree as ET
import re

### START CHANGES HERE

### the AIN of the device (without blanks)
AIN="1234567890"

### max. Power
WATTPEAK = 600

### Output-Files
WATTPCT_DAT="wattpct.dat"
TEMPERATURE_DAT="temperature.dat"

### Add the data of your Fritz!Box
url = "http://fritz.box/"

# credentials to logon to Fritz!Box
username = "<user>"
password = "<password>"

### END CHANGES HERE


### constant
HTTP_OK = 200

### Login
### Get challenge to create response
api_response = requests.get(url+"login_sid.lua?username="+username)
response_xml = ET.fromstring(api_response.text)

### SID already set?
for item in response_xml.findall('./SID'):
	SID = item.text

### create SID
if (SID == "0000000000000000"):
	for item in response_xml.findall('./Challenge'):
		challenge = item.text

	### Create response for Login
	md5 = hashlib.md5()
	md5.update(challenge.encode('utf-16le'))
	md5.update('-'.encode('utf-16le'))
	md5.update(password.encode('utf-16le'))
	response = challenge + '-' + md5.hexdigest()

	api_response = requests.get(url+"login_sid.lua?username="+username+"&response="+response)
	response_xml = ET.fromstring(api_response.text)

	### Get SID
	for item in response_xml.findall('./SID'):
		SID = item.text

### read Sensordata

### Energy
if (SID != "0000000000000000"):
	url_ain=url+"/webservices/homeautoswitch.lua?ain="+ AIN + "&switchcmd=getswitchpower&sid="+SID

	api_response = requests.get(url_ain)

	if (api_response.status_code == HTTP_OK):
		watt = api_response.text

		re.sub('\n','', watt)

		watt = float(watt) / 1000

		### act. Power in pct
		wattpct = round(watt / WATTPEAK * 100,2)

		### debug
		print ('watt:' + str(watt))
		print ('wattpct:' + str(wattpct))

		### File-Output
		datei = open(WATTPCT_DAT,'w')
		datei.write(str(wattpct))

### Temperature
if (SID != "0000000000000000"):
	url_ain=url+"/webservices/homeautoswitch.lua?ain="+ AIN + "&switchcmd=gettemperature&sid="+SID

	api_response = requests.get(url_ain)

	if (api_response.status_code == HTTP_OK):
		temperature = api_response.text

		re.sub('\n','', temperature)

		temperature = float(temperature) / 10

		### debug
		print ('temperature:' + str(temperature))

		### File-Output
		datei = open(TEMPERATURE_DAT,'w')
		datei.write(str(temperature))

### END
