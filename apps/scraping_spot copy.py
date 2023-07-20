
from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

from mongo_db import ConnectDB

#一休から取得
url = "https://www.ikyu.com/kankou/area8010/"


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#DB接続
db = ConnectDB('points_of_interest','spot_list')

i = 0
spot_list = []
for elem in soup.find_all('li', class_="itemlist-li"):
    if(i < 30):#30件のみ
        detail_url = urljoin(url,elem.a['href'])
        response = requests.get(detail_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        name = soup.find('h1','this-title inlineblock').text.strip()
        address = soup.select_one('.this-address').find('td').text.strip()
        recommendation = True
        
        spot_list.append({'name' : name, 'address' : address, 'rec' : str(recommendation)})
        
        sleep(1)
        
        i += 1
        
db.create(spot_list)
db.read()
db.close()

# print(spot_list)