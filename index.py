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

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("success汉字测试：index")
    def post(self):
        print("首页：")
        postDict = json.loads(self.request.body)
        print(postDict)
        self.set_header("Content-Type", "text/plain")
        if postDict['credential'] == users[postDict['ID']]:
            db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
            cursor = db.cursor()
#             sql="select * from user_info where id='%s' "%(postresult['ID'])        
            sql = f"select * from 用户信息表 where 学号 = '{postDict['ID']}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            res = json.dumps(result)
            cursor.close()
            self.write(res)
            
        else:
            self.write('0')

# class IndexHandler(tornado.web.RequestHandler):       #首页
#     def get(self):
#         self.write("success汉字测试2")

#     def post(self):
#         print("首页：")
#         bodyString = str(self.request.body, encoding="UTF-8")
#         postresult=json.loads(self.request.body)
#         print(postresult)
#         self.set_header("Content-Type", "text/plain")
#         if postresult['credential']==users[postresult['ID']]:
#             connection = pymysql.connect(host='localhost',user='root',password='123456',database='aaa',charset='utf8')  
#             cursor=connection.cursor()
#             sql="select * from user_info where id='%s' "%(postresult['ID'])        
#             cursor.execute(sql)
#             result=cursor.fetchone()
#             a=json.dumps(result)
#             cursor.close()
#             self.write(a)
#         else:
#             self.write('0')
#         self.flush
