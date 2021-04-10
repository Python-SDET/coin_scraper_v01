import requests
from bs4 import BeautifulSoup
import re
import os

baseurl = 'https://www.pcgs.com/'

r = requests.get(baseurl+'coinfacts')
soup = BeautifulSoup(r.content, 'lxml')

# This gives us 12 coin types
coin_headers = soup.find_all('div', class_='box')

# Get Dollars
dollar_header = None
for coin_header in coin_headers:
    coin_type = coin_header.find_all("a", href=re.compile("coinfacts/category"))[0].contents[0]
    if coin_type == 'Dollars':
        dollar_header = coin_header
        break

# Get Morgan Dollars
morgan_link = dollar_header.find_all("a", href=re.compile("coinfacts/category/morgan"))

# Navigate to Morgan Dollars
r = requests.get(baseurl + morgan_link[0]['href'])
dollar_type_soup = BeautifulSoup(r.content, 'lxml')
issue_links = dollar_type_soup.find_all("a", href=re.compile("coinfacts/coin/"))

for issue_link in issue_links:

    link_href = issue_link['href']
    arr_link_href = link_href.split(r'/')
    arr_link_href.insert(len(arr_link_href)-1, 'images')
    images_link = '/'.join(arr_link_href)
    r = requests.get(baseurl + images_link)
    soup_images = BeautifulSoup(r.content, 'lxml')

    images = soup_images.find_all('a', href=re.compile(".jpg"))

    for image in images:
        grade = image['data-sub-html'][3:-4]
        link = image['href']
        responsive = image.find_all('img')
        desc = responsive[0]['alt']
        arr_file_name = link.split(r'/')
        file_name = desc + '~' + grade + '~' + arr_file_name[-1]
        file_name = file_name.replace(r'/', '-')
        os.chdir(r'/home/dw/Pictures/pcgs/')
        with open(file_name, 'wb') as f:
            im = requests.get(link)
            f.write(im.content)
