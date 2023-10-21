#!/usr/bin/python3
# -*- coding: utf-8 -*-

from re import findall
from os import remove
from os import listdir
from os import path
from os.path import isfile
from os.path import isdir
from sys import argv

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem # Для состояний
from aiogram.contrib.fsm_storage.memory import MemoryStorage # Хранилище состояний
from aiogram.contrib.middlewares.logging import LoggingMiddleware # Логгирование
from aiogram.types.menu_button import MenuButton, MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault, MenuButtonType # Menu Button
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.markdown import hide_link # hide_link('https://telegra.ph/file/562a512448876923e28c3.png')

from config_reader import config
from logger import logger
#from db import BD
from messages import *
from file import *
from other import *

# Состояния:
#   main
#   doc_peoples
#   doc_users
#   doc_spheres
#   doc_event_\d+
#   text_event_\d+
#   text_search_surname
#   text_search_tag
#   send_all

# Объект бота
bot = Bot(token=config.BOT_TOKEN.get_secret_value())
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())
# База данных
#bd = BD(config.SQL_PATH.get_secret_value())

# Команды

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    try:
        if id in getUsersKeys():
            if isAccess(id):
                data = getUsers()
                data[id]["username"] = username
                setUsers(data)

                states = getStateData()
                states[id]["state"] = "main" # setState
                states[id]["sphere"] = ""
                setState()

                logger.info(getLog('+', f"Info about user with id = {id} updated"))
        else:
            data = getUsers()
            data[id] = {
                "username": username,
                "access": False,
                "admin": False
            }
            setUsers(data)

            states = getStateData()
            states[id] = {
                "state": "main",
                "sphere": ""
            }
            setState()

            logger.info(getLog('+', f"New user with id = {id} and username = {username}"))
    except Exception as e:
        await errorMessage(bot, message, e)

    if isAccess(id):
        await getCmdStartMessage(bot, message)
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    if isAccess(message.from_user.id):
        try:
            setState(message.from_user.id, "main")
            await getCmdHelpMessage(bot, message)
        except Exception as e:
            await errorMessage(bot, message, e)
    else:
        await blockMessage(bot, message)


@dp.message_handler(commands=["admin"])
async def cmd_admin(message: types.Message):
    id = message.from_user.id
    if isAccess(id):
        try:
            setState(id, "main")
            if isAdmin(id):
                await getCmdAdminMessage(bot, message)
            else:
                await getCmdNoAdminMessage(bot, message)
        except Exception as e:
            await errorMessage(bot, message, e)
    else:
        await blockMessage(bot, message)

@dp.message_handler(commands=["main"])
async def cmd_main(message: types.Message):
    if isAccess(message.from_user.id):
        try:
            await getMainMessage(bot, message)
            setState(message.from_user.id, 'main')
        except Exception as e:
            await errorMessage(bot, message, e)
    else:
        await blockMessage(bot, message)

# Текст

@dp.message_handler()
async def text_message(message: types.Message):
    if isAccess(message.from_user.id):
        if isAdmin(message.from_user.id):
            try:
                if isState(message.from_user.id, "text_search_surname"):
                    await getContactSurnameMessage(bot, message, message.text)
                elif isState(message.from_user.id, "text_search_tag"):
                    await getContactTagMessage(bot, message, message.text)
                elif (len(findall("text_event_\d+", getState(message.from_user.id))) == 1):
                    num = int(getState(message.from_user.id).split('_')[-1])
                    data = getEvents()
                    data[num]["description"] = message.text
                    setEvents(data)
                    await getSuccessfulyEditEventMessage(bot, message)
                    setState(message.from_user.id, "main")
                elif isState(message.from_user.id, 'send_all'):
                    await getAllMessage(bot, message, message.text)
                    await getSuccessfulySendAllMessage(bot, message)
                    setState(message.from_user.id, 'main')
                else:
                    await errorSendingTextMessage(bot, message)
            except Exception as e:
                await errorMessage(bot, message, e)
        else:
            await getCmdNoAdminMessage(bot, message)
    else:
        await blockMessage(bot, message)

# Фото

@dp.message_handler(content_types=['photo'])
async def handle_photo(message):
    if isAccess(message.from_user.id):
        if isAdmin(message.from_user.id):
            try:
                await errorSendingPhotoMessage(bot, message)
            except Exception as e:
                await errorMessage(bot, message, e)
        else:
            await getCmdNoAdminMessage(bot, message)
    else:
        await blockMessage(bot, message)

# Документы

@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def document_message(doc: types.document.Document):
    if isAccess(doc.from_user.id):
        try:
            if isAdmin(doc.from_user.id):
                if isState(doc.from_user.id, "doc_peoples"):
                    if doc["document"]["mime_type"] == "application/json":
                        if doc["document"]["file_size"] < 180000: # ~1000 peoples
                            file_id = doc['document']['file_id']
                            file = await bot.get_file(file_id)
                            file_path = file.file_path
                            test_file_path = f'data/test_{doc.from_user.id}.json'
                            await bot.download_file(file_path, test_file_path)
                            error = isCorrectPeoples(test_file_path)
                            if error == "":
                                contentPathToPeoples(test_file_path)
                                await successfulyEditedMessage(bot, doc)
                                setState(doc.from_user.id, "main")
                            else:
                                await errorEditedMessage(bot, doc, f"Ошибка: {error}")

                            remove(test_file_path)
                        else:
                            await errorEditedMessage(bot, doc, "Подобный файл не может быть такого размера")
                    else:
                        await errorEditedMessage(bot, doc, "Файл должен быть .json")
                elif isState(doc.from_user.id, "doc_users"):
                    if doc["document"]["mime_type"] == "application/json":
                        if doc["document"]["file_size"] < 200000:
                            file_id = doc['document']['file_id']
                            file = await bot.get_file(file_id)
                            file_path = file.file_path
                            test_file_path = f'data/test_{doc.from_user.id}.json'
                            await bot.download_file(file_path, test_file_path)
                            error = isCorrectUsers(test_file_path)
                            if error == "":
                                contentPathToUsers(test_file_path)
                                await successfulyEditedMessage(bot, doc)
                                setState(doc.from_user.id, "main")
                            else:
                                await errorEditedMessage(bot, doc, f"Ошибка: {error}")

                            remove(test_file_path)
                        else:
                            await errorEditedMessage(bot, doc, "Подобный файл не может быть такого размера")
                    else:
                        await errorEditedMessage(bot, doc, "Файл должен быть .json")
                elif isState(doc.from_user.id, "doc_spheres"):
                    if doc["document"]["mime_type"] == "application/json":
                        if doc["document"]["file_size"] < 1024:
                            file_id = doc['document']['file_id']
                            file = await bot.get_file(file_id)
                            file_path = file.file_path
                            test_file_path = f'data/test_{doc.from_user.id}.json'
                            await bot.download_file(file_path, test_file_path)
                            error = isCorrectSpheres(test_file_path)
                            if error == "":
                                contentPathToSpheres(test_file_path)
                                await successfulyEditedMessage(bot, doc)
                                setState(doc.from_user.id, "main")
                            else:
                                await errorEditedMessage(bot, doc, f"Ошибка: {error}")

                            remove(test_file_path)
                        else:
                            await errorEditedMessage(bot, doc, "Подобный файл не может быть такого размера")
                    else:
                        await errorEditedMessage(bot, doc, "Файл должен быть .json")
                elif (len(findall("doc_event_\d+", getState(doc.from_user.id))) == 1):
                    if doc["document"]["mime_type"].split('/')[0] == "image":
                        if doc["document"]["file_size"] < 52000000: # ~50 мбайт
                            file_type = doc["document"]["mime_type"].split('/')[-1]
                            num = getState(doc.from_user.id).split('_')[-1]
                            file_id = doc['document']['file_id']
                            file = await bot.get_file(file_id)
                            file_path = file.file_path
                            for x in listdir('media'):
                                if f'event_{num}' in x:
                                    remove(f'media/{x}')
                            await bot.download_file(file_path, f'media/event_{num}.{file_type}')
                            data = getEvents()
                            data[int(num)]['path'] = f'media/event_{num}.{file_type}'
                            setEvents(data)
                            await getEventDescriptionMessage(bot, doc, num)
                            setState(doc.from_user.id, f"text_event_{num}")
                        else:
                            await errorEditedMessage(bot, doc, "Нельзя загружать настолько большие изображения")
                    else:
                        await errorEditedMessage(bot, doc, "Возможно загрузить только изображения")
                else:
                    await errorSendingFileMessage(bot, doc)
            else:
                await getCmdNoAdminMessage(bot, doc)
        except Exception as e:
            test_file_path = f"data/test_{doc.from_user.id}"
            if isfile(test_file_path):
                remove(test_file_path)
            await errorMessage(bot, doc, e)
    else:
        await blockMessage(bot, doc)

# Callbacks

@dp.callback_query_handler(lambda callback_query: True)
async def callback(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id

    if isAccess(id):
        #try:
        if True:
            admin = isAdmin(id)
            setState(id, "main")

            if callback_query.data == "back":
                await getBack(callback_query)
            elif callback_query.data == 'main':
                await getMainMessage(bot, callback_query)
            elif callback_query.data == 'spheres':
                await getSpheresResendMessage(callback_query)
            elif callback_query.data == 'search_surname':
                setState(id, "text_search_surname")
                await getSearchSurnameResendMessage(callback_query)
            elif callback_query.data == 'search_tag':
                setState(id, "text_search_tag")
                await getSearchTagResendMessage(callback_query)
            elif callback_query.data == 'events':
                await getEventsResendMessage(bot, callback_query)
            elif callback_query.data == 'edit_peoples' and admin:
                setState(id, "doc_peoples")
                await getPeoplesEditMessage(bot, callback_query)
            elif callback_query.data == 'edit_users' and admin:
                setState(id, "doc_users")
                await getUsersEditMessage(bot, callback_query)
            elif callback_query.data == 'edit_spheres' and admin:
                setState(id, "doc_spheres")
                await getSpheresEditMessage(bot, callback_query)
            elif callback_query.data == 'edit_events' and admin:
                await getEventsEditMessage(callback_query)
            elif callback_query.data == 'back_to_admin_panel' and admin:
                await getBackToAdminPanelMessage(callback_query)
            elif callback_query.data in getSpheres():
                await getOneSphereMessage(callback_query, callback_query.data)
            elif callback_query.data in list(getPeoples().keys()):
                await getContactResendMessage(callback_query, callback_query.data)
            elif callback_query.data == 'edit_events_append' and admin:
                data = getEvents()
                max_i = 0
                try:
                    max_i = max(list(data.keys()))
                except Exception:
                    pass
                data[max_i + 1] = {
                    "path": "",
                    "description": ""
                }
                setEvents(data)
                await getEventsEditMessage(callback_query)
            elif callback_query.data == 'edit_events_delete' and admin:
                data = getEvents()
                max_i = 0
                try:
                    max_i = max(list(data.keys()))
                except Exception:
                    pass

                if max_i > 0:
                    del data[max_i]
                    setEvents(data)
                    for x in listdir('media'):
                        if f'event_{max_i}' in x:
                            remove(f'media/{x}')
                await getEventsEditMessage(callback_query)
            elif (len(findall("event_\d+", callback_query.data)) == 1) and admin:
                setState(id, f"doc_event_{callback_query.data.split('_')[-1]}")
                await getEventChangeMessage(callback_query)
            elif (len(findall("edit_events_text_empty_\d+", callback_query.data)) == 1) and admin:
                num = int(callback_query.data.split('_')[-1])
                data = getEvents()
                data[num]["description"] = ""
                setEvents(data)
                await getSuccessfulyEditEventMessage(bot, callback_query)
            elif callback_query.data == 'message_all' and admin:
                setState(id, 'send_all')
                await bot.send_message(callback_query.from_user.id, "Введите текст сообщения", reply_markup=getBackToMainButton())
        #except Exception as e:
            #await errorMessage(bot, callback_query, e)
    else:
        await blockMessage(bot, callback_query)

# Служебные

async def on_startup(dp):
    await set_default_commands(dp)
    logger.info(getLog('=', "<-START->"))

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('main', 'Главное меню'),
            types.BotCommand('admin', 'Открыть панель Администратора'),
            types.BotCommand('help', 'Помощь')
        ]
    )

def getLog(s, text):
    return f"bot.py : [{s}] {text}"

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    #del bd
    shutdown(dp)
    logger.info(getLog('=', "<-STOP->"))
