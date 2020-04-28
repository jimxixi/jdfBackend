
# import platform
# if platform.system() == "Windows":
#     import asyncio
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# import tornado.ioloop
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

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("success汉字测试：login")
    def post(self):
        print("登陆：")
        # bodyString = str(self.request.body)
        postDict = json.loads(self.request.body)
        print(postDict)
        self.set_header("Content-Type", "text/plain")
        db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
        cursor = db.cursor()
#         sql="select * from user_info where id='%s' AND password='%s'"%(postresult['ID'],postresult['password'])        
        sql = f"select * from 用户信息表 where 学号='{postDict['ID']}' AND 密码='{postDict['password']}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        credential = makeUUID()
        if result == None:
            self.write('0')
        else:
            self.write('1\n')
            self.write(credential)
            users[postDict['ID']]=credential
            print(users)
        #self.write(json.dumps({"result": "1"}))

# class LoginHandler(tornado.web.RequestHandler):     #登陆
#     def get(self):
#         self.write("success汉字测试1")

#     def post(self):
#         print("登陆：")
#         bodyString = str(self.request.body, encoding="UTF-8")
#         postresult=json.loads(self.request.body)
#         print(postresult)
#         self.set_header("Content-Type", "text/plain")
#         connection = pymysql.connect(host='localhost',user='root',password='123456',database='aaa',charset='utf8')   #连接数据库
#         cursor=connection.cursor()
#         sql="select * from user_info where id='%s' AND password='%s'"%(postresult['ID'],postresult['password'])        
#         cursor.execute(sql)
#         result=cursor.fetchone()
#         cursor.close()
#         credential=makeUUID()
#         if result==None:
#             self.write('0')
#         else:
#             self.write('1\n')
#             self.write(credential)
#             users[postresult['ID']]=credential
#             print(users)
#         #self.write(json.dumps({"result": "1"}))
#         self.flush
