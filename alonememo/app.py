from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

#크롤링하기 위한 2줄
import requests
from bs4 import BeautifulSoup

#mongodb 쓰기전 꼭 import하기
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': 'GET 연결 완료!'})

#리스팅 하는 부분
@app.route('/memo', methods=['GET']) #메모란을 get 요청
def listing(): #db의 아티클 부분 다 찾아서
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'all_articles':articles}) #all_articles로 태워서 내려줌줌


## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])#서버쪽에, /memo, POST 라는 API가 있음
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

###크롤링
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers) #페이지 정보를 가져온 뒤

    soup = BeautifulSoup(data.text, 'html.parser') #그것을 bs4에 넣고 솎아내기 좋은 html형식으로

    title = soup.select_one('meta[property="og:title"]')['content'] #og:title, content 속성값만 가지고 와라
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
###하는 부분

###DB에 저장하는
    doc = { #DOC을 만들어서
        'title':title,
        'image':image,
        'desc':desc,
        'url':url_receive,
        'comment':comment_receive
    }

    db.articles.insert_one(doc) #Mongodb에 저장하는 형태
###부분

    return jsonify({'msg':'저장이 완료되었습니다!'}) #alert response로 "메시지" 뜸

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)