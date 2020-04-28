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

class QueryProductHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("success查询商品列表")
    def post(self):
        print("查询商品列表：")
        argDict = json.loads(self.request.body)
        print(argDict)
        if argDict['credential'] == users[argDict['ID']]:
            db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
            cursor = db.cursor()
            sql = f'select * from 商品清单 where 商品状态=1'
            cursor.execute(sql)
            result = cursor.fetchall()
            productList = []
            for product in result:
                product = list(product)
                product[2] = int(product[2])
                product = tuple(product)
                productList.append(product)
            print("查询到商品数：" + str(len(result)))
            a = json.dumps(productList)
            cursor.close()
            self.write(a)
        else:
            self.write('0')

# class QueryProductHandler(tornado.web.RequestHandler):     # 查询商品列表
#     def get(self):
#         self.write("success汉字测试8")

#     def post(self):
#         print("查询商品列表：")
#         bodyString = str(self.request.body, encoding="UTF-8")
#         argDict = json.loads(self.request.body)
#         print(argDict)
#         if argDict['credential'] == users[argDict['ID']]:
#             connection = pymysql.connect(host='localhost',user='root',password='123456',database='aaa',charset='utf8') 
#             cursor=connection.cursor()
#             # sql="select * from bill_info where id='%s' "%(postresult['ID'])
#             sql = f'select * from product_list where goods_state = "1"'
#             cursor.execute(sql)
#             result=cursor.fetchall()
#             print("查询到商品数：" + str(len(result)))
#             a = json.dumps(result)
#             cursor.close()
#             self.write(a)
#         else:
#             self.write('0')
