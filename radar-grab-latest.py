#!/bin/python
#
# Downloads the latest meteorological radar image of hungary
# 
# Requirements: requests 
#

import requests
import datetime
import os.path

time = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
time = datetime.datetime(
	time.year, 
	time.month, 
	time.day, 
	time.hour, 
	time.minute - time.minute % 15)

filename = 'RccW' + time.strftime('%Y%m%d_%H%M') + '.jpg';
outfilename = 'images/' + filename

if not os.path.exists(outfilename):
	url = 'http://www.met.hu/img/RccW/' + filename
	r = requests.get(url)
	if r.status_code == 200:
		with open(outfilename, 'w+') as f:
			f.write(r.content)
