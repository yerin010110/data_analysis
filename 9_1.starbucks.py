
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def fetch_starbucks():
    url = 'https://www.starbucks.co.kr/index.do'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)

    # ActionChains(): 마우스나 키보드와 같은 복잡한 사용자 상호작용을 시뮬레이션하는 데 사용
    # 매장 CSS_selector: #gnb > div > nav > div > ul > li.gnb_nav03 > h2 > a
    action = ActionChains(driver)
    first_tag = driver.find_element(By.CSS_SELECTOR, '#gnb > div > nav > div > ul > li.gnb_nav03') # 글자와 a태그는 필요가 없어서 영역까지만 가져오기

    # 플로트 후 CSS_selector: #gnb > div > nav > div > ul > li.gnb_nav03 > div > div > div > ul:nth-child(1) > li:nth-child(3) > a
    second_tag = driver.find_element(By.CSS_SELECTOR, '#gnb > div > nav > div > ul > li.gnb_nav03 > div > div > div > ul:nth-child(1) > li:nth-child(3) > a')

    # first -> sec 이동 후 클릭
    # perform() : 실행해라 ActionChains를 실행
    action.move_to_element(first_tag).move_to_element(second_tag).click().perform()

    seoul_tag = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#container > div > form > fieldset > div > section > article.find_store_cont > article > article:nth-child(4) > div.loca_step1 > div.loca_step1_cont > ul > li:nth-child(1) > a")))
    seoul_tag.click()

    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "set_gugun_cd_btn")))
    gu_elements = driver.find_elements(By.CLASS_NAME, "set_gugun_cd_btn")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mCSB_2_container > ul > li:nth-child(1) > a")))
    gu_elements[0].click()

    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quickResultLstCon"))) # li가 뜨기 전 진행이 되면 csv 파일로 저장이 제대로 안들어옵니다!

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    stores = soup.find('ul', 'quickSearchResultBoxSidoGugun').find_all('li')

    store_list = []
    addr_list = []
    lat_list = []
    lng_list = []

    for store in stores:
        store_name = store.find('strong').text
        store_addr = store.find('p').text
        store_addr = re.sub(r'\d{4}-\d{4}$', '', store_addr).strip() # '\d{4}-\d{4}$' 4자-4자
        store_lat = store['data-lat'] # 각 매장별 위경도
        store_lng = store['data-long'] # 각 매장별 위경도
        store_list.append(store_name)
        addr_list.append(store_addr)
        lat_list.append(store_lat)
        lng_list.append(store_lng)

    df = pd.DataFrame({
        'store': store_list,
        'addr': addr_list,
        'lat': lat_list,
        'lng': lng_list
    })

    driver.quit()
    return df


starbucks_df = fetch_starbucks()
starbucks_df.to_csv("starbucks_seoul.csv", index=False, encoding='utf-8-sig')
print('데이터가 starbucks_seoul.csv 파일로 저장되었습니다.')




