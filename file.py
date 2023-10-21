#!/usr/bin/python3
# -*- coding: utf-8 -*-

from json import dump
from json import load

def getJsonData(file_name):
    with open(file_name, 'r') as file:
        data = load(file)

    if file_name in ['data/users.json', 'data/events.json', 'data/states.json']:
        return convertJsonDataToKeyInt(data)

    return data

def writeJsonData(file_name, data):
    with open(file_name, 'w', encoding='utf8') as file:
        dump(data, file, ensure_ascii=False, indent=4)

def convertJsonDataToKeyInt(data):
    new = {}
    for x in data.keys():
        new[int(x)] = data[x]

    return new

def getData(file_name):
    with open(file_name, 'r') as file:
        data = file.read()

    return data

def setData(file_name, data):
    with open(file_name, 'w') as file:
        file.write(data)