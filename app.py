import time
from selenium import webdriver

from selenium.webdriver.common.by import By 
from  selenium.webdriver.support  import  expected_conditions  as  ec
from  selenium.webdriver.support.ui  import  WebDriverWait 
import json

def crawlerLMEMetal(url):
    try:
        option = webdriver.ChromeOptions()
        # 【參考】https://ithelp.ithome.com.tw/articles/10244446
        # option.add_argument("headless") # 不開網頁搜尋(這個必須開啟)
        option.add_argument('blink-settings=imagesEnabled=false') # 不加載圖片提高效率
        option.add_argument('--log-level=3') # 這個option可以讓你跟headless時網頁端的console.log說掰掰
        """下面參數能提升爬蟲穩定性"""
        option.add_argument('--disable-dev-shm-usage') # 使用共享內存RAM
        option.add_argument('--disable-gpu') # 規避部分chrome gpu bug

        # driver = webdriver.Chrome(chrome_options=option) #啟動模擬瀏覽器
        driver = webdriver.Chrome(cromedriver_path, chrome_options=option) #啟動模擬瀏覽器
        driver.get(url) # 取得網頁代碼

        # 隐性等待30秒 (只要寫一次即可) => 等頁面渲染完才會抓
        driver.implicitly_wait(30)


        # https://gist.github.com/miodeqqq/b416b42e1573e6d35f464375297a070c
        # find iframe (顯性等待 10秒)
        captcha_iframe = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(
                (By.TAG_NAME, 'iframe')
            )
        )

        # 跳轉至 iframe中
        driver.switch_to.frame(captcha_iframe)

        # 載入完之後=> 找到<input>並進行 click
        input_tag = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(
                (By.TAG_NAME, 'input')
            )
        )

        # 點擊
        input_tag.click()

        # 點擊完等待一下
        # time.sleep(3)


        # 跳出 iframe
        driver.switch_to.default_content()

        # 捕捉最後結果 <pre>中的 JSON資料
        pre = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(
                (By.TAG_NAME, 'pre')
            )
        )

        # text 轉成 json
        json_data = json.loads(pre.text)
        return json_data

    except KeyboardInterrupt:
        print("----(已中斷程式)----")

    except Exception as e:
        print(f"捕捉資料發生錯誤: {e}")

    finally: # 最終都會關閉 chromedriver
        driver.close()
        driver.quit()

        



if __name__ == "__main__":
    # url = 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=5ff6f336-bd23-40c5-bcce-2e038d652f99'
    cromedriver_path = './chromedriver.exe'

    # API連結
    steel_dict = {
        '廢鋼': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=5ff6f336-bd23-40c5-bcce-2e038d652f99',
        '特種鋁合金': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=2dea7bc8-37e2-4381-b97f-fbd72748b1e4', 
        # '金': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=70b0fc72-facb-458d-8fa1-43aa66cf894e', # Precious metals → LME Gold
        '鈷': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=2b5439b2-f8c0-4b3b-8bf7-ba2a851f00ab',
        '鉛': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=bc443de6-0bdd-4464-8845-9504f528b0c6',
        # '銀': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=78c5915e-aae1-4114-be4f-88da565bef57', # Precious metals → LME Silver
        '銅': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=762a3883-b0e1-4c18-b34b-fe97a1f2d3a5',
        '鋁': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=1a0ef0b6-3ee6-4e44-a415-7a313d5bd771',
        '鋁合金': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=a60d3ff3-3a17-4b8c-8476-5e8dd0c9b713', 
        '鋅': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=c389e2b0-c4a3-46a0-96ca-69cacbe90ee4', # Zinc
        '鋼筋': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=f894524d-cadf-404b-995a-e9a19f49d394',
        '錫': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=361d4046-e7b6-4043-af80-8ce9cbee6727',
        '鎳': 'https://www.lme.com/api/trading-data/day-delayed?datasourceId=acadf037-c13f-42f2-b42a-cac9a8179940'
    }

    for name, url in steel_dict.items():

        json_data = crawlerLMEMetal(url)
        if json_data:
            print(f"{name}.....✅成功捕捉")

        # 儲存JSON檔案(中文字處理)
        # https://blog.csdn.net/baidu_36499789/article/details/121371587
        to_path = f"json/{name}.json"
        json_object = json.dumps(json_data, indent=4, ensure_ascii=False)
        with open(to_path, "w", encoding="utf8") as outfile:
            outfile.write(json_object)
    
    print("================================")
    print("執行完成，視窗即將在兩秒之後關閉...")
    time.sleep(2)