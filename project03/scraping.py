from flask import Flask
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests

app = Flask(__name__)

client = MongoClient('3.35.24.64', 27017, username="test", password="test")
db = client.dbsparta_plus_week3


driver = webdriver.Chrome('./chromedriver') #셀레니움이 크롬드라이버를 잡아서

url = "http://matstar.sbs.co.kr/location.html" #맛집 페이지

driver.get(url) #url 데리고 와서
time.sleep(5)

#페이지 소스 로드하기 전에 더 많은 맛집정보 가져오기 위해, 더보기 선택자 만들기
# btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button") #css 선택자를 가지고 요소를 찾는다
# btn_more.click() #더보기 클릭
# time.sleep(5)

for i in range(10): #더보기 10번 누르기
    try:
        btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(5)
    except NoSuchElementException: #try 코드 실행하다가 예외 발생시
        break

req = driver.page_source #페이지 소스 로드
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

places = soup.select("ul.restaurant_list > div > div > li > div > a") #카드의 선택자, places 안에 맛집 목록 저장
print(len(places))

for place in places:
    title = place.select_one("strong.box_module_title").text #상점 간판 제목
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text #식당 주소
    category = place.select_one("div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text #식당의 카테고리 
    show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)#몇 번째의 어떤 에피소드?
    print(title, address, category, show, episode)

    headers = {
        "X-NCP-APIGW-API-KEY-ID": "mtjbr1c0cc",
        "X-NCP-APIGW-API-KEY": "bnqCQTyNDQCRP8NWfkKnyhKEYkIlzRm8U4SxiEJh"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers) #쿼리 부분에 주소, requests.get요청시 headers로 보내준다
    response = r.json()


    if response["status"] == "OK": #ok라면
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"]) #그냥 꺼내면 문자열로 나와서 실수값으로
            y = float(response["addresses"][0]["y"])
            print(title, address, category, show, episode, x, y)

            doc = { #DB 저장
                "title": title,
                "address": address,
                "category": category,
                "show": show,
                "episode": episode,
                "mapx": x,
                "mapy": y}
            db.matjips.insert_one(doc)

        else:
            print(title, "좌표를 찾지 못했습니다")