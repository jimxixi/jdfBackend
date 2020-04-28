import tornado.web
import os
import pymysql
import json
import time
import uuid
import PaySimTool
import random

from stuSideLib import users



# util
def makeTimeStamp() -> str:
    # 生成时间戳的工具
    return str(int(1000 * time.time()))

def makeUUID() -> str:
    # 生成唯一编码的凭据
    return str(uuid.uuid4())


class ScholarshipHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("奖学金: scholarship")
    def post(self):
        print("奖学金：")
        postDict = json.loads(self.request.body)
        print(postDict)
        self.set_header("Content-Type", "text/plain")
        if postDict['credential'] == users[postDict['ID']]:
            db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
            cursor = db.cursor()
            sql = f"select * from 奖学金信息表 where 学号='{postDict['ID']}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            res = []
            for record in result:
                record = list(record)
                record[5] = str(record[5])
                record[6] = str(record[6])
                res.append(record)
            cursor.close()
            self.write(json.dumps(res))
        else:
            self.write('0')


