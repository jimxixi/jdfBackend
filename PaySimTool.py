
import urllib.request
import json


PayServerURL = "http://127.0.0.1:20056/PaySim"

def _post(url: str, data: dict) -> dict:
    req = urllib.request.Request(url, data=bytes(json.dumps(data), encoding="UTF-8"), method="POST")
    response = urllib.request.urlopen(req)
    # print(response.read().decode("UTF-8"))
    resDict = json.loads(response.read())
    # print(resDict)
    return resDict


def TryCreateTransaction(target: str, source: str, tradeID: str, sum: int, timeLimit: int) -> dict:
    return _post(PayServerURL, {
        "method": "发起交易",
        "target": target,
        "source": source,
        "tradeID": tradeID,
        "sum": sum,
        "timeLimit": timeLimit,
    })

def CheckTransaction(tradeID: str) -> dict:
    return _post(PayServerURL, {
        "method": "查询交易",
        "tradeID": tradeID,
    })



