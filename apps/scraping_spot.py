
from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

from mongo_db import ConnectDB

#一休から取得
url = "https://www.ikyu.com/kankou/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#DB接続
db = ConnectDB('points_of_interest','spot_list')

i = 0 #都道府県の数の数ループ
#TOPページから各都道府県のページへ飛ぶ
for area in soup.find_all('li', class_="itemlist-li"):
    if(i < 3):#47都道府県***********************************************
        area_name = area.find('h3', class_="itemlist-li-item__title").text.strip()
        area_url = urljoin(url, area.a["href"])
        
        #エリア毎のページに遷移
        area_response = requests.get(area_url)
        area_soup = BeautifulSoup(area_response.text, 'html.parser')

        #エリア毎にリスト初期化
        spot_list = []
        j = 0 #各エリア30件取得
        for elem in area_soup.find_all('li', class_="itemlist-li"):
            if(j < 5): #エリア30件********************************************
                detail_url = urljoin(url,elem.a['href'])
                detail_response = requests.get(detail_url)
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                
                name = detail_soup.find('h1','this-title inlineblock').text.strip()
                address = detail_soup.select_one('.this-address').find('td').text.strip()
                recommendation = True
                
                spot_list.append({'area' : area_name, 'name' : name, 'address' : address, 'rec' : str(recommendation)})
                
                sleep(1)
                
                j += 1
        #print(spot_list)
        i += 1
        db.create(spot_list)
        #db.read()
        db.close()