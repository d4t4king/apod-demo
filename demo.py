#!/usr/bin/python

import argparse
import re
import requests
import pprint
from urlparse import urlparse
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

initial_url = 'https://apod.nasa.gov/apod/archivepix.html'
r = requests.get(initial_url)
if r.status_code == 200:
    soup = BeautifulSoup(r.content, "html.parser")
    print("HTML Title: " + str(soup.title))
else:
    print("We didn't get a good return code: " + r.status_code)
