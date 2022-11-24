from flask import Flask, request, send_file
import redis
from analyze import funshii
import json
from flask_cors import CORS
import pickle
from random import sample
import os
app = Flask(__name__,static_folder=os.path.dirname(__file__)+'picture/')
CORS(app)
pool = redis.ConnectionPool(host='redis-10516.c299.asia-northeast1-1.gce.cloud.redislabs.com',password='9slS8BIAJWQ7C51q0Te4qt22wZwO1UYn', port=10516, db=0)
localpool = redis.ConnectionPool(host="localhost",port=6380,db=0)
r = redis.Redis(connection_pool=pool,decode_responses=True,charset='UTF-8',encoding='UTF-8')
photoUrl = "https://funshii.zeabur.app/photo?keyword="
print(r.ping())

@app.route('/')
def index():
    # key 為 test 的資料 +1
    # r.hgetall('核能')
    # 取得 test 的資料
    test = r.ping()
    return test
@app.route('/search')
def search():
    keyword = request.args.get("keyword",None)
    if(keyword==""):
        return "no keywords"
    result = r.hgetall(keyword)
    result= {key.decode('utf-8'):value.decode('utf-8') for key,value in result.items()}
    print(result)
    # print(json.loads(result))
    # print(type(json.loads(result)))
    if(len(result)>0):
        r.close()
        return json.dumps({'category':result['category'],'textCloud':photoUrl+result['category'],'title':result['title'],'link':result['link'],'date':result['date'],'keywords':json.loads(result['keywords'])},ensure_ascii=False)
    else:
        result = funshii(keyword)
        r.hmset(keyword,{'category':keyword,'title':result.title,'link':result.link,'date':result.date,'keywords':json.dumps(result.keywords,ensure_ascii=False)})
        # r.hset(keyword,"title",result.title)
        # r.hset(keyword,"link",result.link)
        # r.hset(keyword,"result",result.result)
        r.close()
        return json.dumps({'category':keyword,'textCloud':photoUrl+keyword,'title':result.title,'link':result.link,'date':result.date,'keywords':result.keywords},ensure_ascii=False)
@app.route('/huh')
def huh():
    keylist=sample(r.keys("*"),5)
    list = []
    for i in range(len(keylist)):
        keylist[i] = keylist[i].decode('utf-8')
        print(keylist[i])
        hot = r.hgetall(keylist[i])
        hot= {key.decode('utf-8'):value.decode('utf-8') for key,value in hot.items()}
        list.append({'category':hot['category'],'textCloud':photoUrl+hot['category'],'title':hot['title'],'link':hot['link'],'date':hot['date'],'keywords':json.loads(hot['keywords'])})
    print(keylist)

    # list.append({'category':buffet['category'],'title':buffet['title'],'link':buffet['link'],'date':buffet['date'],'keywords':json.loads(buffet['keywords'])})
    return json.dumps(list,ensure_ascii=False)
@app.route('/photo')
def photo():
    keyword = request.args.get("keyword",None)
    file = os.getcwd() +'/picture/'+ keyword +'.png'
    return send_file(file)
if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)