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


class QueryPaymentRecord(tornado.web.RequestHandler):
    def get(self):
        self.write("查询缴费记录")
    def post(self):
        print("查询订单缴费记录：")
        postDict = json.loads(self.request.body)
        print(postDict)
        self.set_header("Content-Type", "application/json")
        responseList = []
        if postDict['credential'] == users[postDict['ID']]:
            db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
            cursor = db.cursor()
#             sql = "select * from bill_info where id='%s' "%(postresult['ID'])
            sql = f"select * from 订单信息表 where 学号='{postDict['ID']}' order by 订单编号 desc"
            cursor.execute(sql)
            billInfoList = cursor.fetchall()
            print("订单数：", len(billInfoList))
            payment_state_dict = {
                '0': "支付失败",
                '1': "支付成功",
                '2': "选缴-待缴",
                '3': "必缴-待缴",
                '4': "选缴-超时",
                '5': "必缴-超时",
            }
            for billInfo in billInfoList:
                billDict = {
                    'bill_id': str(billInfo[0]),
                    'payment_state': payment_state_dict[billInfo[6]],
                    'create_timestamp': str(billInfo[3]),
                    'isPaid': False,
                    'bill_price': str(billInfo[2]),
                    'subBillList': [],
                }
                if billInfo[6] == '1':
                    billDict['isPaid'] = True
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
                        "remark": "数量：" + str(subBill[3]),
                    })
                responseList.append(billDict)
            self.write(json.dumps(responseList))
            print("缴费记录查询结果：", len(responseList))
            cursor.close()
        else:
            self.write("0")

# class QueryPaymentRecord(tornado.web.RequestHandler):       # 查询缴费记录
#     def get(self):
#         self.write("查询缴费记录")
#     def post(self):
#         print("查询订单缴费记录")
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
#             payment_state_dict = {
#                 '0': "支付失败",
#                 '1': "支付成功",
#                 '2': "选缴-待缴",
#                 '3': "必缴-待缴",
#                 '4': "选缴-超时",
#                 '5': "必缴-超时",
#             }
#             for billInfo in billInfoList:
#                 billDict = {
#                     'bill_id': billInfo[0],
#                     'payment_state': payment_state_dict[billInfo[5]],
#                     'create_timestamp': billInfo[3],
#                     'isPaid': False,
#                     'bill_price': billInfo[2],
#                     'subBillList': [],
#                 }
#                 if billInfo[5] == '1':
#                     billDict['isPaid'] = True
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
#             print("缴费记录查询结果: ", responseList)
#             cursor.close()
#         else:
#             self.write("0")
