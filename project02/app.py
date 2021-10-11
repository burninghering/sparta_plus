from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import requests


app = Flask(__name__)

client = MongoClient('3.35.24.64', 27017, username="test", password="test")
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    msg=request.args.get("msg")
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    words = list(db.words.find({}, {"_id": False}))
    return render_template("index.html", words=words,msg=msg) #템플릿 만들때 보내줌


@app.route('/detail/<keyword>') #주소 URL의 일부(앞부분만)받아
def detail(keyword):
    status_receive=request.args.get("status_give")
    #keyword 라는 변수로 저장을 해서 요청을 보내는 URL뒤에 넣어준 뒤, header 정보 안에 내 토큰을 넣어준다
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token ed4c16e8cab27f9cf2587dcba3c60d9a2a89a0ee"})

    if r.status_code!=200:
        return redirect(url_for("main", msg="단어가 이상합니다!")) #현재 요청된 연결을 특정 주소로 재연결

    result = r.json()
    print(result)
    return render_template("detail.html", word=keyword,result=result,status=status_receive) #detail/ 뒤에 오는 단어를 word로 보냄


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receive=request.form['word_give'] #post요청이기에 request, word_give로 보내줄게!
    definition_receive = request.form['definition_give']
    doc={
        "word":word_receive,"definition":definition_receive
    }
    db.words.insert_one(doc)
    return jsonify({'result': 'success', 'msg': f'단어 {word_receive} 저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receive = request.form["word_give"]
    db.words.delete_one({"word":word_receive})
    return jsonify({'result': 'success', 'msg': f'단어 {word_receive}삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)