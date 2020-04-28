import platform
if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import tornado.ioloop
import tornado.web
import os
import pymysql
import json
import time
import uuid
import PaySimTool
import random


from login import LoginHandler
from index import IndexHandler
from reset import ResetHandler
from enquiry import EnquiryHandler
from createpayment import CreatepaymentHandler
from pay import PayHandler
from checkpay import CheckpayHandler
from queryProduct import QueryProductHandler
from queryPaymentRecord import QueryPaymentRecord
from scholarship import ScholarshipHandler

# # util
# def makeTimeStamp() -> str:
#     # 生成时间戳的工具
#     return str(int(1000 * time.time()))

# def makeUUID() -> str:
#     # 生成唯一编码的凭据
#     return str(uuid.uuid4())

from stuSideLib import users

def main():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    app = tornado.web.Application([
        (r'/logging', LoginHandler),
        (r'/index', IndexHandler),
        (r'/reset', ResetHandler),
        (r'/enquiry', EnquiryHandler),
        (r'/createpayment', CreatepaymentHandler),
        (r'/queryPaymentRecord', QueryPaymentRecord),
        (r'/pay', PayHandler),
        (r'/checkpay', CheckpayHandler),
        (r'/queryProduct', QueryProductHandler),
        (r'/scholarship', ScholarshipHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {"path": settings['static_path']}),
    ])
    app.listen(20113)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print('running')
    main()

