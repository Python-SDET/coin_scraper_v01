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
link_1878_8tf = issue_links[0]['href']
arr_link_1878_8tf = link_1878_8tf.split(r'/')
arr_link_1878_8tf.insert(len(arr_link_1878_8tf)-1, 'images')
images_link_1878_8tf = '/'.join(arr_link_1878_8tf)
r = requests.get(baseurl + images_link_1878_8tf)
soup_images_1878_8tf = BeautifulSoup(r.content, 'lxml')

images = soup_images_1878_8tf.find_all('img', class_='img-responsive lazy')

for image in images:
    name = image['alt']
    link = image['data-src']
    arr_file_name = link.split(r'/')
    file_name = name + arr_file_name[-1]
    os.chdir(r'/home/dw/Pictures/pcgs/')
    with open(file_name, 'wb') as f:
        im = requests.get(link)
        f.write(im.content)
