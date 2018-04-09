from flask import Flask, request
import json
import requests
import pandas as pd
import numpy as np

before = ""
con = ""
# ตรง YOURSECRETKEY ต้องนำมาใส่เองครับจะกล่าวถึงในขั้นตอนต่อๆ ไป
# test read file
data = pd.read_excel("testexcel.xlsx")
#vendor
vendor = []
vendor.append(data['Unnamed: 0'][2])
vendor.append(data['Unnamed: 0'][6])
vendor.append(data['Unnamed: 0'][10])
#configuration
config_hua = []
for i in range(2,6) :
    config_hua.append(data['Unnamed: 1'][i])
config_nok = []
for i in range(6,10) :
    config_nok.append(data['Unnamed: 1'][i])
config_eric = []
for i in range(10,14) :
    config_eric.append(data['Unnamed: 1'][i])
#Huawei BB and RRU
hua_BB = dict()
hua_RRU = dict()
for i in range(4) :
    hua_BB[config_hua[i]] = []
    hua_RRU[config_hua[i]] = []
    for j in range(2,6) :
        if j == 2 :
            temp = "FDD"
        else :
            temp = 'Unnamed: ' + str(j)
        hua_BB[config_hua[i]].append(data[temp][i+2])
    for j in range(2,6) :
        temp = 'Unnamed: ' + str(j+4)
        hua_RRU[config_hua[i]].append(data[temp][i+2])
#Nokia BB and RRU
nok_BB = dict()
nok_RRU = dict()
for i in range(4) :
    nok_BB[config_nok[i]] = []
    nok_RRU[config_nok[i]] = []
    for j in range(2,6) :
        if j == 2 :
            temp = "FDD"
        else :
            temp = 'Unnamed: ' + str(j)
        nok_BB[config_nok[i]].append(data[temp][i+6])
    for j in range(2,6) :
        temp = 'Unnamed: ' + str(j+4)
        nok_RRU[config_nok[i]].append(data[temp][i+6])
# Ericsson BB and RRU
eric_BB = dict()
eric_RRU = dict()
for i in range(4) :
    eric_BB[config_eric[i]] = []
    eric_RRU[config_eric[i]] = []
    for j in range(2,6) :
        if j == 2 :
            temp = "FDD"
        else :
            temp = 'Unnamed: ' + str(j)
        eric_BB[config_eric[i]].append(data[temp][i+10])
    for j in range(2,6) :
        temp = 'Unnamed: ' + str(j+4)
        eric_RRU[config_eric[i]].append(data[temp][i+10])
# end test
global LINE_API_KEY
LINE_API_KEY = "Bearer VeZxZ+55VcOWLNra3BBOua8ORc6nzDn76baWmG1cs6MlI2RsjzGbmIansUQ81BF09HwBPatKDSzCO0QXkRcImHZLEBBlh8px09Y5+JSLlEM004HJAQ2NRcuUlr51OpOnwYgcqMHqAfBt0vqte4DH+gdB04t89/1O/w1cDnyilFU="
app = Flask(__name__)
 
@app.route('/')
def index():
    return 'This is chatbot server.'
@app.route('/bot', methods=['POST'])

def bot():
    # ข้อความที่ต้องการส่งกลับ
    global before
    global con
    global vendor
    global config_hua
    global config_eric
    global config_nok
    global hua_RRU
    global hua_BB
    global nok_RRU
    global nok_BB
    global eric_RRU
    global eric_BB
    replyStack = list()
   
    # ข้อความที่ได้รับมา
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)
    
    # Token สำหรับตอบกลับ (จำเป็นต้องใช้ในการตอบกลับ)
    replyToken = msg_in_json["events"][0]['replyToken']

    # ทดลอง Echo ข้อความกลับไปในรูปแบบที่ส่งไป-มา (แบบ json)
    replyStack.append(msg_in_string)
    # answer
    
    if msg_in_json["events"][0]["message"]["text"] == "Vendor" :
        reply(replyToken, vendor)
    elif msg_in_json["events"][0]["message"]["text"] in vendor :
        reply(replyToken, ["Ok, I know what your mobile is."," If you want to about configuration.","Please, type Configuration."])
    elif msg_in_json["events"][0]["message"]["text"] == "Configuration" :
        if before == "Huawei" :
            config_hua.append("What is your configuration?")
            reply(replyToken, config_hua)
        elif before == "Nokia" :
            config_nok.append("What is your configuration?")
            reply(replyToken, config_nok)
        else :
            "What you want to know next? BB or RRU?"
            config_eric.append("What is your configuration?")
            reply(replyToken, config_eric)
    elif msg_in_json["events"][0]["message"]["text"] in config_hua :
        con = msg_in_json["events"][0]["message"]["text"]
        before = list()
        before.append(hua_BB)
        before.append(hua_RRU)
        #before = [hua_BB,hua_RRU]
        reply(replyToken, ["Is it BB or RRU"])
    elif msg_in_json["events"][0]["message"]["text"] in config_nok :
        con = msg_in_json["events"][0]["message"]["text"]
        before = [nok_BB,nok_RRU]
        reply(replyToken, ["Is it BB or RRU"])
    elif msg_in_json["events"][0]["message"]["text"] in config_eric :
        con = msg_in_json["events"][0]["message"]["text"]
        before = [eric_BB,eric_RRU]
        reply(replyToken, ["Is it BB or RRU"])
    elif msg_in_json["events"][0]["message"]["text"] in ["BB","RRU"] :
        if msg_in_json["events"][0]["message"]["text"] == "BB" :
            if len(before) == 2 :
                before = before[0]
                t = '2'
            else :
                before = nok_BB
                t = '0'
            reply(replyToken, ["What is your sector?"])
        else :
            before = before[1]
            reply(replyToken, ["What is your sector?"])
    elif len(msg_in_json["events"][0]["message"]["text"].strip().split()) == 2 :
        temp = int(msg_in_json["events"][0]["message"]["text"].strip().split()[0])
        if temp == 3 :
            tmp = before[con][0]
            before = ""
            con = ""
            reply(replyToken, [tmp])
        elif temp == 4 :
            tmp = before[con][1]
            before = ""
            con = ""
            reply(replyToken, [tmp])
        elif temp == 6 :
            tmp = before[con][2]
            before = ""
            con = ""
            reply(replyToken, [tmp])
        else :
            tmp = before[con][3]
            before = ""
            con = ""
            reply(replyToken, [tmp])

    else :
        before = ""
        con = ""
        reply(replyToken, ["Please, input Vendor first."])
    
    return 'OK',200

def reply(replyToken, textList):
    # Method สำหรับตอบกลับข้อความประเภท text กลับครับ เขียนแบบนี้เลยก็ได้ครับ
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text":text
        })
    data = json.dumps({
        "replyToken":replyToken,
        "messages":msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    return

if __name__ == '__main__':
    app.run()
