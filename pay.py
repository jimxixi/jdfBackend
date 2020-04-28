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

class PayHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("请求支付")
    def post(self):
        print("请求支付：")
        postDict = json.loads(self.request.body)
        print(postDict)

        res = PaySimTool.TryCreateTransaction("测试账户2", "测试账户1", postDict['bill_id'], 2, 30)
        print("PaySimTool.TryCreateTransaction: ", res)
        self.write(res['transactionID'])

# class PayHandler(tornado.web.RequestHandler):           # 请求支付
#     def get(self):
#         self.write("请求支付")
#     def post(self):
#         print("请求支付：")
#         bodyString = str(self.request.body, encoding="UTF-8")
#         postresult = json.loads(self.request.body)
#         print(postresult)

#         res = PaySimTool.TryCreateTransaction("测试账户2", "测试账户1", postresult['bill_id'], 2, 30)
#         print("PaySimTool.TryCreateTransaction: ", res)
#         self.write(res['transactionID'])



