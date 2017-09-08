#!/usr/bin/python

import argparse
import re
import requests
import pprint
import datetime
import os.path
from urlparse import urlparse
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

args_parse = argparse.ArgumentParser(description="Get those images!")
args_parse.add_argument('-y', '--year', dest='search_year', type=int, help='Specify the year for which you would like to collect images.')
args_parse.add_argument('-m', '--month', dest='search_mon', type=int, help='Specify the month for which you would like to collect images.')
args_parse.add_argument('-d', '--dir', dest='savedir', help='Specify the directory to save the images to.  (Defaults to current directory.)')
args = args_parse.parse_args()

#now = datetime.datetime.now()

if args.search_year:
	if len(str(args.search_year)) == 4:
		print('Got a full year')
		print('trimming it down...')
		args.search_year = str(args.search_year)[2:]
	elif len(str(args.search_year)) == 2:
		print('Got a Y2K year')
	else:
		print('Unrecognized year length')
else:
	args.search_year = "".join(list(str(datetime.datetime.now().year))[2:4])
print('YEAR: ' + str(args.search_year))
print('MONTH: ' + str(args.search_mon))

if str(args.search_mon) == 'None':
	fnpatt = r"ap" + str(args.search_year) + "\d?.*?\d\d\.html"
else:
	fnpatt = r"ap" + str(args.search_year) + "\d?" + str(args.search_mon) + "\d\d\.html"
print("PATTERN: " + fnpatt)
fnp_re = re.compile(fnpatt)
stub_url = 'https://apod.nasa.gov/apod'
initial_url = stub_url + '/archivepix.html'
r = requests.get(initial_url)
pages = list()
if r.status_code == 200:
	soup = BeautifulSoup(r.text, "html.parser")
	for link in soup.find_all("a"):
		#print("|" + link.get('href') + "|")
		if re.search(fnp_re,link.get('href')):
			page_url = stub_url + '/' + link.get('href')
			print(page_url)
			pages.append(page_url)
else:
	print("We didn't get a good return code: " + r.status_code)

for u in pages:
	ur = requests.get(u)
	usoup = BeautifulSoup(ur.text, "html.parser")
	for ulnk in usoup.find_all('img'):
		print(stub_url + '/' + ulnk.parent.get('href'))
		filename = os.path.basename(ulnk.parent.get('href'))
                if not args.savedir:
                    args.savedir = "."
                local_path = args.savedir + "/" + filename
		img = requests.get(stub_url + '/' + ulnk.parent.get('href'), stream=True)
		print('FILE: ' + local_path)
		if img.status_code == 200:
			with open(local_path, 'wb') as f:
				for chunk in img:
					f.write(chunk)
		else:
			print("Got HTTP code " + str(img.status_code) + " while trying to download image.")

