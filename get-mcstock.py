#!/usr/bin/env python3

#Original code from here: https://forum.level1techs.com/t/automated-microcenter-stock-checking-updated/117256
#Modifications only made to data parsing (for updated Micro Center Website) and replacing email notif with discord

import re
import requests
from time import sleep
import pickle
import os
import json

cookies = dict(storeSelected='121')
global inStockItems
itemURLs = []
global msgText
msgText = ""
stockCurrent = {}
if os.path.exists("items_in_stock"):
    stockLast = pickle.load(open(r"items_in_stock", "rb"))
    

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect
    def removed(self):
        return self.set_past - self.intersect
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

URLS = [
   'https://www.microcenter.com/product/613206/asus-x570-i-rog-strix-amd-am4-mini-itx-motherboard',
   'https://www.microcenter.com/product/608673/gigabyte-x570-aorus-amd-am4-mitx-motherboard'
    ]

def send_discord(msg):
    webhook_url = 'DISCORDWEBHOOKURLHERE'
    requests.post(webhook_url, data=json.dumps({ "content": msg }), headers={ 'Content-Type': 'application/json',})

for item in URLS:
    respData = requests.get(item, cookies=cookies).text
    skuNum = re.findall(r"'SKU':(.*?),",str(respData))
    print(skuNum[0])
    inStock = re.findall(r"'inStock':(.*?),",str(respData))
    #inStock = ["'True'"] #Uncomment to test a successful run
    print(inStock[0])
    productPrice = re.findall(r"'price':(.*?),",str(respData))
    print(productPrice[0])
    storeId = re.findall(r"'storeNum':(.*?),",str(respData))
    brand = re.findall(r"'brand':(.*?),",str(respData))
    print(storeId[0])
    print(stockCurrent)
    stockCurrent[skuNum[0].replace("'",'')] = inStock[0].replace("'",'')
    for stock in inStock:
        print(stock)
        if stock == "'True'":
            msgText = msgText+brand[0].replace("'",'')+" -- SKU: "+skuNum[0].replace("'",'')+" -- "+productPrice[0].replace("'",'')+"\n"+item+"\n\n"
        elif stock == "'False'":
            print("SKU: "+skuNum[0].replace("'",'')+" -- Out of stock")
        else:
            print("Error retrieving stock")
    sleep(5)

with open(r"items_in_stock", "wb") as outfile:
    pickle.dump(stockCurrent, outfile)

stockDiff = DictDiffer(stockCurrent, stockLast).changed()

if stockDiff:
    print("Stock changed:")
    for i in stockDiff:
        if stockCurrent[i] == "False":
            print(i+" -- "+"Out of stock")
        elif stockCurrent[i] == "True":
            print(i+" -- "+"IN STOCK")
else:
    print("Stock unchanged")

storeInfo="""Paste store address and other info here"""

if len(msgText) and stockDiff:
    print(msgText)
    send_discord(msgText)
else:
    print("No message sent")
del inStock,msgText