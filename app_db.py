import pymysql #資料庫套件
import requests
import time
from bs4 import BeautifulSoup
import json
import os

def connect_db(host, user, pwd, dbname, port):
    try:
        db = pymysql.connect(
            host = host,
            user = user,
            passwd = pwd,
            database = dbname,
            port = int(port)
        )
        # print("連線成功")
        return db
    except Exception as e:
        print('連線資料庫失敗: {}'.format(str(e)))
    return None

def UpdateMetalHover(name, price, hoverValue):
    with db.cursor() as cursor:
        try:
            
            cursor.execute(
                "UPDATE lme_metal_prices SET MetalPrice = %s, MetalDate = %s, enabled = '1' WHERE MetalName = %s",
                (price, hoverValue, name)
            )
            db.commit()
            return True
        
        except Exception as e:
            print(f"UpdateMetalHover發生不明錯誤: {e}")

def UpdateMetalEnabled(name):
    with db.cursor() as cursor:
        try:
            cursor.execute(
                "UPDATE lme_metal_prices SET enabled = '0' WHERE MetalName = %s",
                (name)
            )
            db.commit()
            return True
        
        except Exception as e:
            print(f"UpdateMetalEnabled發生不明錯誤: {e}")
    
 

if __name__ == "__main__":
    db = connect_db(
        '127.0.0.1',
        'root',
        'Ru,6e.4vu4wj/3',
        'greenhouse',
        3306,
    ) # 資料庫連線

    if( not db ):
        print("資料庫連線發生問題")
        
    
    # json 檔案連結
    steel_dict = {
        '廢鋼': '廢鋼.json',
        '特種鋁合金': '特種鋁合金.json',
        '鈷': '鈷.json',
        '鉛': '鉛.json',
        '銅': '銅.json',
        '鋁': '鋁.json',
        '鋁合金': '鋁合金.json',
        '鋅': '鋅.json',
        '鋼筋': '鋼筋.json',
        '錫': '錫.json',
        '鎳': '鎳.json',
    }

    # 一一讀取 JSON檔案
    for name, filename in steel_dict.items():
        path = os.path.join(os.getcwd(), 'json', filename)
        print(name)

        with open(path, mode='r', encoding='utf8') as f:
            json_data = json.load(f)
            
            if("Rows" in json_data):
                if( len(json_data['Rows']) > 0 ):
                    price = json_data['Rows'][0]['Values'][0] # 價格
                    hover_value = json_data['Rows'][0]['HoverValue'] # 懸停值
                    BusinessDateTime = json_data['Rows'][0]['BusinessDateTime'] # 懸停值
                    # print(f"名稱: {name} ； 價格: {price } ； HoverValue: {hover_value}")
                    print(f"名稱: {name} ； 價格: {price } ； HoverValue: {hover_value} ； BusinessDateTime: {BusinessDateTime}")
                    UpdateMetalHover(name, price, BusinessDateTime)
                    
            else:
                print(f'名稱: {name} ； 發生錯誤: {json_data["Message"]}')
                UpdateMetalEnabled(name)

        

        print("--------------")
    
    print("程式執行結束，3秒後將關閉")
    time.sleep(3)


