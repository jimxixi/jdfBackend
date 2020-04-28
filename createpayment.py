import tornado.web
import os
import pymysql
import json
import time
import datetime
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

class CreatepaymentHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("success汉字测试：createpayment")
    def post(self):
        print("生成选缴订单：")
        reqList = json.loads(self.request.body)
        print(reqList)
        if reqList[0]['credential'] == users[reqList[0]['ID']]:
            db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf8')
            cursor = db.cursor()
            # 首先，创建订单，或许应该先创建订单，然后再创建每个子订单。
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql3 = f"insert into 订单信息表 \
                (创建时间, 学号, 订单支付状态, 支付渠道) values \
                    ('{t}', '{reqList[0]['ID']}', '2', '模拟银联支付')"
            print("插入订单：" + sql3)
            cursor.execute(sql3)
            db.commit()
            # 然后，获取自增的订单编号
            sql1 = f"select LAST_INSERT_ID()"
            cursor.execute(sql1)
            orderid = cursor.fetchone()[0]
            sum = 0
            # 最后，遍历请求中的商品，为它们创建子订单
            for sub_bill in reqList[1:]:
                sql = f"select * from 商品清单 where 商品编号='{sub_bill['goods_id']}'"
                cursor.execute(sql)
                product = cursor.fetchone()
                sum += product[2]
                sql2 = f"insert into 子订单信息表 \
                    (子订单编号, 订单编号, 商品编号, 商品数量, 商品单价, 子订单总额, 商户代码) values \
                        ('{makeUUID()}', {orderid}, '{sub_bill['goods_id']}', {int(sub_bill['num'])}, {product[2]}, {int(sub_bill['num']*product[2])}, '{product[3]}') "
                cursor.execute(sql2)
                db.commit()
            sql = f"update 订单信息表 set 交易金额={sum} where 订单编号={orderid}"
            cursor.execute(sql)
            db.commit()
            cursor.close()
            self.write('1')
        else:
            print("创建选缴订单时校验失败")
            self.write('0')


# class CreatepaymentHandler废弃(tornado.web.RequestHandler):
#     def get(self):
#         self.write("success汉字测试：createpayment")
#     def post(self):
#         print("生成选缴订单：")
#         reqList = json.loads(self.request.body)
#         print(reqList)
#         if reqList[0]['credential'] == users[reqList[0]['ID']]:
#             db=pymysql.connect(host='localhost',user='root',password='123456',database='db20200213',charset='utf-8')
#             cursor = db.cursor()
#             # TODO: 以下三行是应用程序实现自增逻辑，如果数据库自带自增逻辑，那么就检查是否必要获取数据库的自增指标。
#             # sql = "select * from bill_info order by orderid desc limit 1"
#             sql = f"select * from 订单信息表 order by 订单编号 desc limit 1"
#             cursor.execute(sql)
#             # 把 mysql里面的bigInt 转换为 int，可能多余。
#             newOrderid = int(cursor.fetchone()[0]) + 1
#             # sum = 0
#             # new Orderid = makeUUID()
#             for sub_bill in reqList[1:]:
# #                 sql = "select * from product_list where goodsid='%s' "%(sub_bill['goods_id'])
#                 sql = f"select * from 商品清单 where 商品编号='{sub_bill['goods_id']}'"
#                 cursor.execute(sql)
#                 product = cursor.fetchone()
#                 # sum += product[2]
# #                 sql2 = "INSERT INTO sub_bill_info VALUES ('%s','%s','%s','%s','%s','%s','%s') "%(makeUUID(),newOrderid,sub_bill['goods_id'],str(sub_bill['num']),(product[2]),str(product[2]+"*"+str(sub_bill['num'])),product[3])
#                 # TODO: 如果自增逻辑由数据库实现，这里去掉订单编号。
#                 # TODO: 下列 1 行代码重点测试
#                 sql2 = f"insert into 子订单信息表 values ('{makeUUID}', '{newOrderid}', '{sub_bill['goods_id']}', '{sub_bill['num']}', '{product[2]}', '{product[2]*sub_bill['num']}', '{product[3]}')"
#                 cursor.execute(sql2)
#                 db.commit()
# #             sql3="INSERT INTO bill_info VALUES ('%s','%s','%s','%s','%s','%s','%s','%s') "%(newOrderid,"",str(product[2]+"*"+str(sub_bill['num'])),makeTimeStamp(),reqList[0]['ID'],"2",None,None)
#             # TODO: 下列 1 行语句需要针对新表结构重写
#             sql3 = f"insert into bill_info values ('{newOrderid}', '', '{product[2]*sub_bill['num']}', '{makeTimeStamp()}', '{reqList[0]['ID']}', '2', '{None}', '{None}')"
#             print("插入订单：" + sql3)
#             cursor.execute(sql3)
#             db.commit()
#             cursor.close()
#             self.write('1')
#         else:
#             print("校验失败")

#             self.write('0')


# class CreatepaymentHandler(tornado.web.RequestHandler):         # 创建选缴订单
#     def get(self):
#         self.write("success汉字测试5")
#     def post(self):
#         print("生成选缴订单：")
#         bodyString = str(self.request.body, encoding="UTF-8")
#         reqList = json.loads(self.request.body)
#         print(reqList)
#         if reqList[0]['credential'] == users[reqList[0]['ID']]:
#             connection = pymysql.connect(host='localhost',user='root',password='123456',database='aaa',charset='utf8')
#             cursor = connection.cursor()
#             # sql = "select * from bill_info order by orderid desc limit 1"
#             # cursor.execute(sql)
#             # newOrderid = int(cursor.fetchone()[0]) + 1
#             newOrderid = makeUUID()
#             for sub_bill in reqList[1:]:
#                 sql = "select * from product_list where goodsid='%s' "%(sub_bill['goods_id'])
#                 cursor.execute(sql)
#                 product = cursor.fetchone()
#                 sql2 = "INSERT INTO sub_bill_info VALUES ('%s','%s','%s','%s','%s','%s','%s') "%(makeUUID(),newOrderid,sub_bill['goods_id'],str(sub_bill['num']),(product[2]),str(product[2]+"*"+str(sub_bill['num'])),product[3])
#                 cursor.execute(sql2)
#                 connection.commit()
#             sql3="INSERT INTO bill_info VALUES ('%s','%s','%s','%s','%s','%s','%s','%s') "%(newOrderid,"",str(product[2]+"*"+str(sub_bill['num'])),makeTimeStamp(),reqList[0]['ID'],"2",None,None)
#             print("插入订单：" + sql3)
#             cursor.execute(sql3)
#             connection.commit()
#             cursor.close()
#             self.write("1")
#         else:
#             print("校验失败")
#             self.write('0')
