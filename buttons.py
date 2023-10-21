#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from other import getSpheres
from other import getPeoples
from other import getEvents

def getCmdStartButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Начать", callback_data="back"))
    return markup

def getMainButtons():
    markup = InlineKeyboardMarkup(row_width=2)
    button0 = InlineKeyboardButton('Сферы', callback_data='spheres')
    button1 = InlineKeyboardButton('Поиск по фамилии', callback_data='search_surname')
    button2 = InlineKeyboardButton('Поиск по нику(tg)', callback_data='search_tag')
    button3 = InlineKeyboardButton('Мероприятия', callback_data='events')
    markup.add(button0, button1, button2, button3)
    return markup

def getInlineButtonBackToMain():
    return InlineKeyboardButton("↩️ Вернуться в главное меню", callback_data='back')

def getInlineButtonToMain():
    return InlineKeyboardButton("↩️ Вернуться в главное меню", callback_data='main')

def getInlineButtonBackToAdmin():
    return InlineKeyboardButton("↩️ Вернуться в панель администратора", callback_data='back_to_admin_panel')

def getSpheresButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToMain()
    markup.add(back)
    list = []
    spheres = getSpheres()
    for x in spheres:
        list.append(InlineKeyboardButton(x, callback_data=x))
    return markup.add(*list)

def getSearchButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToMain()

    markup.add(back)
    return markup

def getEventsButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonToMain()

    markup.add(back)
    return markup

def getLibButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToMain()

    markup.add(back)
    return markup

def getCmdAdminButtons():
    markup = InlineKeyboardMarkup(row_width=2)
    button0 = InlineKeyboardButton("Контакты", callback_data='edit_peoples')
    button2 = InlineKeyboardButton("Мероприятия", callback_data='edit_events')
    button3 = InlineKeyboardButton("Сферы", callback_data='edit_spheres')
    button4 = InlineKeyboardButton("Пользователи", callback_data='edit_users')
    button5 = InlineKeyboardButton("Сообщение всем", callback_data='message_all')

    markup.add(button0, button2, button3, button4, button5)
    return markup

def getPeoplesEditButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToMain()

    markup.add(back)
    return markup

def getSuccessfulyEditedButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToAdmin()

    markup.add(back)
    return markup

def getOneSphereButtons(sphere):
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton("↩️ Вернуться", callback_data="spheres")
    markup.add(back)
    list = []
    peoples = getPeoples()

    for x in peoples.keys():
        if sphere in peoples[x]["sphere"]:
            list.append(InlineKeyboardButton(f"{x} {peoples[x]['name']}", callback_data=x))

    markup.add(*list)
    return markup

def getContactButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToMain()

    markup.add(back)
    return markup

def getContactResendButtons(sphere):
    markup = InlineKeyboardMarkup(row_width=1)
    back = InlineKeyboardButton("↩️ Вернуться", callback_data=sphere)

    markup.add(back)
    return markup

def getEventsEditButtons():
    markup = InlineKeyboardMarkup(row_width=2)
    back = getInlineButtonBackToAdmin()
    markup.add(back)
    append = InlineKeyboardButton("Добавить в конец", callback_data='edit_events_append')
    markup.add(append)
    delete = InlineKeyboardButton("Удалить последнее", callback_data='edit_events_delete')
    markup.add(delete)

    list = []
    data = getEvents()
    for x in data.keys():
        line = f'{x} (Пусто)'
        if data[x]["path"] != "":
            line = f'{x}'
        list.append(InlineKeyboardButton(line, callback_data=f'event_{x}'))

    markup.add(*list)
    return markup

def getEventDescription(num):
    markup = InlineKeyboardMarkup(row_width=1)
    empty = InlineKeyboardButton("Без описания", callback_data=f'edit_events_text_empty_{num}')
    markup.add(empty)

    return markup

def getSuccessfulyEditEventButtons():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToAdmin()
    markup.add(back)

    return markup

def getSuccessfulySendAllButton():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToAdmin()
    markup.add(back)

    return markup

def getBackToMainButton():
    markup = InlineKeyboardMarkup(row_width=1)
    back = getInlineButtonBackToAdmin()
    markup.add(back)

    return markup