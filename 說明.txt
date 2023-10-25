程式抓取的連結： https://www.lme.com/

【虛擬環境】
安裝:『pip install virtualenv』
開啟:『virtualenv <虛擬環境名稱(EX: venv)>』
進入虛擬環境:請在當前專案目錄下執行『.\venv\Scripts\activate』
"""(venv) PS: <當前目錄>: 代表成功"""

● requirements.txt
------------------------------------
使用的函式庫。
如要將函式庫匯出，請執行『pip freeze > requirements.txt』
如需下載函式庫，請執行『pip install -r requirements.txt』


API都已經找好了，一樣 requests跟 BeautifulSoup來去抓資料。

【抓取方式】
1.先瀏覽網頁。https://www.lme.com/en/Metals/Non-ferrous/LME-Zinc#Trading+day+summary
2.打開 Network並重新整理來讀取資料
3.篩選『Fetch/XHR』，找到一個需要的JSON檔
4.點開並查看 Preview中 API的格式來決定要抓哪些資料