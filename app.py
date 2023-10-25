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
        
    cursor = db.cursor()
    # API連結
    steel_dict = {
        # '廢鋼': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=935e2e7d-00ed-4297-a655-0dd492dedf5a',
        # '廢鋼': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=5ff6f336-bd23-40c5-bcce-2e038d652f99',
        # '特種鋁合金': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=2dea7bc8-37e2-4381-b97f-fbd72748b1e4', 
        # '金': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=70b0fc72-facb-458d-8fa1-43aa66cf894e', # Precious metals → LME Gold
        # '鈷': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=2b5439b2-f8c0-4b3b-8bf7-ba2a851f00ab',
        # '鉛': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=bc443de6-0bdd-4464-8845-9504f528b0c6',
        # '銀': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=78c5915e-aae1-4114-be4f-88da565bef57', # Precious metals → LME Silver
        # '銅': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=762a3883-b0e1-4c18-b34b-fe97a1f2d3a5',
        # '鋁': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=1a0ef0b6-3ee6-4e44-a415-7a313d5bd771',
        # '鋁合金': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=a60d3ff3-3a17-4b8c-8476-5e8dd0c9b713', 
        # '鋅': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=c389e2b0-c4a3-46a0-96ca-69cacbe90ee4', # Zinc
        # '鋼筋': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=f894524d-cadf-404b-995a-e9a19f49d394',
        # '錫': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=361d4046-e7b6-4043-af80-8ce9cbee6727',
        # '鎳': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=acadf037-c13f-42f2-b42a-cac9a8179940'
    }
   
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

    for name, filename in steel_dict.items():
        path = os.path.join(os.getcwd(), 'json', filename)
        print(name)
        with open(path, mode='r', encoding='utf8') as f:
            json_data = json.load(f)
            
            if("Rows" in json_data):
                if( len(json_data['Rows']) > 0 ):
                    price = json_data['Rows'][0]['Values'][0] # 價格
                    hover_value = json_data['Rows'][0]['HoverValue'] # 懸停值
                    print(f"名稱: {name} ； 價格: {price } ； HoverValue: {hover_value}")
                    UpdateMetalHover(name, price, hover_value)
                    
            else:
                print(f'名稱: {name} ； 發生錯誤: {json_data["Message"]}')
                UpdateMetalEnabled(name)

        

        print("--------------")
    
    print("程式執行結束，3秒後將關閉")
    time.sleep(3)


