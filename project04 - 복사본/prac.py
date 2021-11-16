from pymongo import MongoClient
#내 컴퓨터에서 돌아가는 db를 사용할 것이다.
client = MongoClient('localhost', 27017)
#dbspart db를 사용할 것이다. 없다면 자동 생성
db = client.dbweling


# 저장 - 예시
doc = {'id': 1,'title': 'title','file': 'file', 'content': 'content', 'postcode': 'postcode', 'roadaddress': 'roadaddress','detailaddress': 'detailaddress','date': 'date'}

db.weling.insert_one(doc)