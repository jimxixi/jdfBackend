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

class ResetHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("success汉字测试：reset")
    def post(self):
        print("修改密码：")
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
            cursor.close()
            if postDict['oldpassword'] == result[8]:
                cursor2 = db.cursor()
#                 sql2="UPDATE user_info SET password='%s' where id='%s' "%(postresult['newpassword'],postresult['ID'])
                sql2 = f"update 用户信息表 set 密码='{postDict['newpassword']}' where 学号='{postDict['ID']}'"
                cursor2.execute(sql2)
                db.commit()
                cursor2.close()
                self.write('1')
            else:
                self.write('0')
        else:
            self.write('0')
# class ResetHandler(tornado.web.RequestHandler):       #修改密码
#     def get(self):
#         self.write("success汉字测试3")

#     def post(self):
#         print("修改密码：")
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
#             cursor.close()
#             if postresult['oldpassword']==result[8]:
#                 cursor2=connection.cursor()
#                 sql2="UPDATE user_info SET password='%s' where id='%s' "%(postresult['newpassword'],postresult['ID'])
#                 cursor2.execute(sql2)
#                 connection.commit()
#                 cursor2.close()    
#                 self.write('1')
#             else:
#                 self.write('0')
#         else:
#             self.write('0')
#         self.flush
