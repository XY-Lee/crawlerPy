import time
from selenium import webdriver
import requests 
from bs4 import BeautifulSoup
import re
import os

url = ''  # 這邊填網址


driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe') # 使用chrome瀏覽器
#time.sleep(3)
driver.get(url)

# resp = requests.get(url)

#dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))
time.sleep(3)
# driver.execute_script("document.getElementsByTagName( 'button' )[2].click()") # 執行 javascript動作
time.sleep(1)
for i in range(60):  # 進行十次
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight*' + str( i * 10 ) + ');')  # 重複往下捲動
    time.sleep(1)  # 每次執行打瞌睡一秒           
    
resp = driver.page_source
soup = BeautifulSoup(resp, 'html.parser')
dcard_title = soup.find_all('h3', re.compile('PostEntry_title_'))   
dcard_href = soup.find_all('a', re.compile('PostEntry_root'))  
count = 0
for index, item in enumerate(dcard_title):
  if "食物" in item.text.strip() :
    driver2 = webdriver.Chrome(executable_path=r'.\chromedriver.exe') # 使用chrome瀏覽器
    print( dcard_href[index]['href'] )
    driver2.get( str( dcard_href[index]['href'] )) ; # 連接上抓出來的網址
    time.sleep(3)  # 每次執行打瞌睡一秒    
    resp2 = driver2.page_source
    soup2 = BeautifulSoup(resp2, 'html.parser')
    dcard_content = soup2.find('div', re.compile('Post_content_'))
    dimg = dcard_content.find_all( 'img' ) # 將圖片tag抓出
    # 載所有圖片
    for iimg in dimg:
      ir = requests.get(iimg['src'])
      if ir.status_code == 200:
        open( str( count ) + '.jpg' , 'wb').write(ir.content)
        count += 1
    driver2.close()
    print("{0:2d}. {1}".format(index + 1, item.text.strip()))
driver.close()  # 關閉瀏覽器

