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

class CheckpayHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("查询支付结果，修改订单状态")
    def post(self):
        print("查询支付结果：")
        postDict = json.loads(self.request.body)
        print(postDict)
        if postDict['credential'] == users[postDict['ID']]:
            transactionID = postDict['odd_number']
            tradeID = postDict['tradeID']
            checkRes = PaySimTool.CheckTransaction(tradeID)
            print("查询支付结果：", checkRes)
            if checkRes['transactionState'] == "已支付":
                print("更新订单状态：")
                db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
                cursor = db.cursor()
#                 sql="UPDATE bill_info SET bill_state='1' where orderid='%s' "%(tradeID)
                sql = f"update 订单信息表 set 订单支付状态='1' where 订单编号='{tradeID}'"
                cursor.execute(sql)
                db.commit()
                cursor.close()
            else:
                self.write('0')

# class CheckpayHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("查询支付结果，修改订单状态")
#     def post(self):
#         print("查询支付结果：")
#         bodyString = str(self.request.body, encoding="UTF-8")
#         postresult = json.loads(self.request.body)
#         print(postresult)
#         if postresult['credential']==users[postresult['ID']]:
#             transactionID = postresult['odd_number']
#             tradeID = postresult['tradeID']
#             checkRes = PaySimTool.CheckTransaction(tradeID)
#             print("查询支付结果：", checkRes)
#             if checkRes['transactionState'] == "已支付":
#                 print("更新订单状态: ")
#                 connection = pymysql.connect(host='localhost',user='root',password='123456',database='aaa',charset='utf8')
#                 cursor=connection.cursor()
#                 sql="UPDATE bill_info SET bill_state='1' where orderid='%s' "%(tradeID)
#                 cursor.execute(sql)
#                 connection.commit()
#                 cursor.close()
#         else:
#             self.write('0')
