#!/usr/bin/python3
# -*- coding: utf-8 -*-

from jsonschema import validate
from json import loads
from json import dumps

from file import getJsonData
from file import writeJsonData
from file import getData
from file import setData
from config_reader import config

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def getUsersKeys():
    return getJsonData(config.USERS_PATH.get_secret_value()).keys()

def getUsers():
    return getJsonData(config.USERS_PATH.get_secret_value())

def setUsers(data):
    writeJsonData(config.USERS_PATH.get_secret_value(), data)

def isAdmin(id):
    return getUsers()[id]["admin"]

def contentPathToPeoples(path):
    data = getJsonData(path)
    writeJsonData(config.PEOPLES_PATH.get_secret_value(), data)

def isCorrectPeoples(path):
    schema = {
        "surname": {
            "name": "name",
            "patronymic": "patronymic",
            "email": "email",
            "phone": "phone",
            "tg": "tg",
            "sphere": ["sphere"],
            "business": "business",
            "position": "position"
        }
    }

    try:
        data = getJsonData(path)
        validate(data, schema)
        keys = data.keys()
        for x in keys:
            l = list(data[x].keys())
            if len(l) != 8:
                return f"Неверное количество свойств у '{x}'"
            else:
                for y in l:
                    if y not in ["name", "phone", "email", "sphere", "tg", "business", "patronymic", "position"]:
                        return f"Неверное свойство '{y}' у '{x}'"
    except Exception as e:
        print(e)
        return e

    return ""

def isState(id, line):
    if getStateData()[id]["state"] == line:
        return True
    else:
        return False

def setState(id, line):
    data = getStateData()
    data[id]["state"] = line
    setStateData(data)

def getState(id):
    return getStateData()[id]["state"]

def getStateData():
    return getJsonData(config.STATES_PATH.get_secret_value())

def setStateData(data):
    writeJsonData(config.STATES_PATH.get_secret_value(), data)

def getSphere(id):
    return getStateData()[id]["sphere"]

def setSphere(id, line):
    data = getStateData()
    data[id]["sphere"] = line
    setStateData(data)

def isAccess(id):
    return getUsers()[id]["access"]

def setAccess(id, b):
    data = getUsers()
    data[id]["access"] = b
    setUsers(data)

def getSpheres():
    return getJsonData(config.SPHERES_PATH.get_secret_value())["spheres"]

def getPeoples():
    return getJsonData(config.PEOPLES_PATH.get_secret_value())

def isCorrectUsers(path):
    schema = {
        123: {
            "username": "username",
            "access": True,
            "admin": True
        }
    }

    try:
        count = 0
        data = getJsonData(path)
        validate(data, schema)
        keys = data.keys()
        for x in keys:
            if data[x]["admin"] == True:
                count += 1
            l = list(data[x].keys())
            if len(l) != 3:
                return f"Неверное количество свойств у '{x}'"
            elif data[x]["admin"] == True and data[x]["access"] == False:
                return f"Администратор не может быть без прав доступа к основному ресурсу ('{x}')"
            else:
                for y in l:
                    if y not in ["username", "access", "admin"]:
                        return f"Неверное свойство '{y}' у '{x}'"
    except Exception as e:
        print(e)
        return e

    if count == 0:
        return "Необходимо наличие минимум одного Администратора"
    else:
        return ""

def contentPathToUsers(path):
    data = getJsonData(path)
    writeJsonData(config.USERS_PATH.get_secret_value(), data)

def isCorrectSpheres(path):
    schema = {
        "spheres": ["first", "second"]
    }

    try:
        data = getJsonData(path)

        if list(data.keys()) != ['spheres']:
            return f"Обнаружены неизвестные ключи {[x for x in list(data.keys()) if x != 'spheres']}"

        validate(data, schema)
    except Exception as e:
        print(e)
        return e

    return ""

def contentPathToSpheres(path):
    data = getJsonData(path)
    writeJsonData(config.SPHERES_PATH.get_secret_value(), data)

def isCorrectEventsConfig(path):
    schema = {
        "file.jpg": "description"
    }

    try:
        data = getJsonData(path)
        validate(data, schema)
        keys = data.keys()
    except Exception as e:
        print(e)
        return e

    return ""

def contentPathToEventsConfig(path):
    data = getJsonData(path)
    writeJsonData(config.EVENTS_PATH.get_secret_value(), data)

def getEvents():
    return getJsonData(config.EVENTS_PATH.get_secret_value())

def setEvents(data):
    writeJsonData(config.EVENTS_PATH.get_secret_value(), data)