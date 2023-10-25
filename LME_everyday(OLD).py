import pymysql #資料庫套件
import requests
import time
from bs4 import BeautifulSoup
import json

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
        '廢鋼': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=5ff6f336-bd23-40c5-bcce-2e038d652f99',
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

    headers = {
        'authority': 'www.lme.com',
        'method': 'GET',
        'path': '/api/trading-data/day-delayed?datasourceId=762a3883-b0e1-4c18-b34b-fe97a1f2d3a5',
        'scheme': 'https',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': 'Not/A)Brand;v=99, Microsoft Edge;v=115, Chromium;v=115',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',    
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',    
        'Referer': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=762a3883-b0e1-4c18-b34b-fe97a1f2d3a5&__cf_chl_tk=xLdM8OBsW.X7VLXqAcxDYCvsjacPTGxE4aNbKp8Gd6g-1691567070-0-gaNycGzNC_s',    
    }


    for name, url in steel_dict.items():
        req = requests.get( url, headers=headers )

        print(req.status_code)
    #     soup = BeautifulSoup(req.text,'html.parser')
    #     response = json.loads(soup.text)
    #     # print(name)
    #     # print(response)

    #     print("------------------------------- ")

    #     if("Rows" in response):
    #         if( len(response['Rows']) > 0 ):
    #             price = response['Rows'][0]['Values'][0] # 價格
    #             hover_value = response['Rows'][0]['HoverValue'] # 懸停值
    #             print(f"名稱: {name} ； 價格: {price } ； HoverValue: {hover_value}")
    #             sql = f"UPDATE lme_metal_prices SET MetalPrice = '{price}', MetalDate = '{hover_value}', enabled = '1' WHERE MetalName = '{name}'"
    #             cursor.execute(sql)    # 將金屬價格寫入資料庫
    #             db.commit()
    #             time.sleep(2) # Delay 2秒，確保不會被當成爬蟲被鎖
    #     else:
    #         print(f'名稱: {name} ； 發生錯誤: {response["Message"]}')
    #         sql = f"UPDATE lme_metal_prices SET enabled = '0' WHERE MetalName = '{name}'"
    #         cursor.execute(sql)    # 將金屬價格寫入資料庫
    #         db.commit()
    #         time.sleep(2) # Delay 2秒，確保不會被當成爬蟲被鎖
    
    # db.close()
    # print("-------------------(寫入完成，關閉資料庫連接)--------------------")