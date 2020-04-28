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


class EnquiryHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("success汉字测试：enquiey")
    def post(self):
        print("查询订单：")
        postDict = json.loads(self.request.body)
        print(postDict)
        self.set_header("Content-Type", "application/json")
        responseList = []
        if postDict['credential'] == users[postDict['ID']]:
            db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
            cursor = db.cursor()
#             sql = "select * from bill_info where id='%s' "%(postresult['ID'])
            sql = f"select * from 订单信息表 where 学号='{postDict['ID']}'"
            cursor.execute(sql)
            billInfoList = cursor.fetchall()
            print("订单数：", len(billInfoList))
            for billInfo in billInfoList:
                billDict = {
                    'bill_id': str(billInfo[0]),
                    'subBillList': [],
                }
#                 sql2 = "select * from sub_bill_info where orderid='%s' "%(billInfo[0])
                sql2 = f"select * from 子订单信息表 where 订单编号='{billInfo[0]}'"
                cursor.execute(sql2)
                subBillList = cursor.fetchall()
                for subBill in subBillList:
#                     sql3 = f'select * from product_list where goodsid="{subBill[2]}"'
                    sql3 = f"select * from 商品清单 where 商品编号='{subBill[2]}'"
                    cursor.execute(sql3)
                    product = cursor.fetchone()
                    billDict['subBillList'].append({
                        "sub_bill_id": subBill[0],
                        "product_id": product[0],
                        "product_name": product[1],
                        "product_price": str(product[2]),
                        "remark": "数量: "+str(subBill[3]),
                    })
                responseList.append(billDict)
            cursor.close()
            self.write(json.dumps(responseList))
        else:
            self.write('0')


# class EnquiryHandler(tornado.web.RequestHandler):       #查询订单
#     def get(self):
#         self.write("success汉字测试4")
#     def post(self):
#         print("查询订单")
#         bodyString = str(self.request.body, encoding="UTF-8")
#         postresult = json.loads(self.request.body)
#         print(postresult)
#         self.set_header("Content-Type", "application/json")
#         responseList = []
#         if postresult['credential'] == users[postresult['ID']]:
#             connection = pymysql.connect(host='localhost',user='root',password='123456',database='aaa',charset='utf8') 
#             cursor = connection.cursor()
#             sql = "select * from bill_info where id='%s' "%(postresult['ID'])
#             cursor.execute(sql)
#             billInfoList = cursor.fetchall()
#             print("订单数：", len(billInfoList))
#             for billInfo in billInfoList:
#                 billDict = {
#                     'bill_id': billInfo[0],
#                     'subBillList': [],
#                 }
#                 sql2 = "select * from sub_bill_info where orderid='%s' "%(billInfo[0])
#                 cursor.execute(sql2)
#                 subBillList = cursor.fetchall()
#                 for subBill in subBillList:
#                     sql3 = f'select * from product_list where goodsid="{subBill[2]}"'
#                     cursor.execute(sql3)
#                     product = cursor.fetchone()
#                     billDict['subBillList'].append({
#                         "sub_bill_id": subBill[0],
#                         "product_id": product[0],
#                         "product_name": product[1],
#                         "product_price": product[2],
#                         "remark": "数量: "+str(subBill[3]),
#                     })
#                 responseList.append(billDict)
#             self.write(json.dumps(responseList))
#             cursor.close()
#         else:
#             self.write("0")
