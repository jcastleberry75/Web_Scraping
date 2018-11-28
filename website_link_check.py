import requests
from bs4 import BeautifulSoup
import datetime
from time import sleep
import os
from colorama import init
from colorama import Fore, Style
from fake_useragent import UserAgent
import urllib3
import hashlib
import json

global found_links
found_links = []
global pages_to_check
pages_to_check = []

# initialize colorama
init(autoreset=True)

# Housekeeping
get_time = datetime.datetime.now()
today_date = get_time.strftime("%Y%m%d")
red = Style.BRIGHT + Fore.RED
cyan = Style.BRIGHT + Fore.CYAN

# create fake user agent, application presents itself to the host as a Chrome Browser
ua = UserAgent()
header = {'user-agent': ua.chrome}

checksums = {}

urllib3.disable_warnings()
print()
print()
def status_check(link):
    sleep(.500)
    #Extended timeout added to allow for slow responses from emory library websites
    response = requests.get(link, headers=header, timeout=9, verify=False, allow_redirects=True)
    status = response.status_code
    print()
    if status == 200:
        print(cyan + link + ' appears to be OK')
        print('Status Code : ' + str(status))
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        tags = soup.find_all('a')
        for tag in tags:
            href = (tag.get('href'))
            found_links.append(href)
        html_code = str(soup.get_text)
        md5_checksum = (hashlib.md5(html_code.encode('utf-8')).hexdigest())
        print('MD% Checksum: ')
        print(md5_checksum)
        checksums[link] = md5_checksum
    else:
        print(red + link + ' appears to have a problem')
        print(red + 'Status Code : ' + str(status))


status_check("http://www.yerkes.emory.edu/")


def link_scraper():
    # Extracting URLs from the attribute href in the <a> tags within the yerkes homepage html and appending list.
    for item in found_links:
        if item is None:
            pass
        elif 'email' in item:
            pass
        elif 'emory'not in item:
            pass
        elif item[0:3] == 'htt':
            if item in pages_to_check:
                pass
            else:
                pages_to_check.append(item)
        else:
            #handles links internal to the yerkes website
            constructed_link = 'http://www.yerkes.emory.edu/' + item
            if item in pages_to_check:
                pass
            else:
                pages_to_check.append(constructed_link)
link_scraper()

print()
print()
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXX THE FOLLOWING LINKS WERE FOUND AT www.yerkes.emory.edu XXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print()
for item in pages_to_check:
    print(item)
print()
print()
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('XXXXXX                CHECKING EMORY LINKS                    XXXXX')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
print()
for item in pages_to_check:
    status_check(item)
    print()
print('CHECK COMPLETE')
print()
print('Checksum Library Created: ')
print(checksums)
#dump checksums to json file
with open(today_date +'_web_checksums.json', 'w') as fp:
    json.dump(checksums, fp)