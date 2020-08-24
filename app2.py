from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('project_2.html')

## API 역할을 하는 부분
@app.route('/hosworks', methods=['POST'])
def write_hosworks():
    # title_receive로 클라이언트가 준 title 가져오기
    day_receive = request.form['day_give']
    # author_receive로 클라이언트가 준 author 가져오기
    works_receive = request.form['works_give']
    # review_receive로 클라이언트가 준 review 가져오기
    etc_receive = request.form['etc_give']

    # DB에 삽입할 review 만들기
    hosworks = {
        'day': day_receive,
        'works': works_receive,
        'etc': etc_receive
    }
    # reviews에 review 저장하기
    db.hosworks.insert_one(hosworks)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success'})


@app.route('/hosworks', methods=['GET'])
def read_hosworks():
    # 1. DB에서 리뷰 정보 모두 가져오기
    hosworks = list(db.hosworks.find({}, {'_id': 0}).sort("day", -1))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'hosworks': hosworks})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)