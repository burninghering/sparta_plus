import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main():
    myname="Sparta"
    return render_template("index.html",name=myname)


@app.route('/detail/<keyword>')
def detail(keyword):
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token ed4c16e8cab27f9cf2587dcba3c60d9a2a89a0ee"})
    result = r.json()
    print(result)

    word_receive=request.args.get("word_give") #get 요청으로 받은 파라미터를 request.args.get로 받기
    print(word_receive)
    return render_template("detail.html",word=keyword)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)