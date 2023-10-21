#!/usr/bin/python3
# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.utils import exceptions

from buttons import *
from config_reader import config
from other import getPeoples
from other import getEvents
from other import getUsers
from other import setState
from other import setSphere
from other import getSphere

async def getBack(callback_query):
    await callback_query.message.edit_text("""Добро пожаловать в <b>бот PBC!</b> 💜

Выберите, что вас интересует:

<b>Сферы</b> - Здесь вы можете найти человека в интересующей вас области деятельности

<b>Мероприятия</b> - Здесь опубликована афиша на текущий месяц

<b>Поиск</b> - Вы можете найти интересующего вас человека по нику в Телеграм/по фамилии""", parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getMainButtons())

async def getMainMessage(bot, message):
    await bot.send_message(message.from_user.id, """Добро пожаловать в <b>бот PBC!</b> 💜

Выберите, что вас интересует:

<b>Сферы</b> - Здесь вы можете найти человека в интересующей вас области деятельности

<b>Мероприятия</b> - Здесь опубликована афиша на текущий месяц

<b>Поиск</b> - Вы можете найти интересующего вас человека по нику в Телеграм/по фамилии""", parse_mode=types.ParseMode.HTML,
                           reply_markup=getMainButtons())

async def getCmdStartMessage(bot, message):
    await bot.send_message(message.from_user.id, "Привет, {0.username}!".format(message.from_user),
                           reply_markup=getCmdStartButtons())

async def getCmdHelpMessage(bot, message):
    await bot.send_message(message.from_user.id, """Как пользоваться ботом PBC:

/main — Открыть главное меню
Сферы - Здесь вы можете найти человека в интересующей вас области деятельности
Мероприятия - Здесь опубликована афиша на текущий месяц
Поиск - Вы можете найти интересующего вас человека по нику в Телеграм/Фамилии""")

async def getCmdAdminMessage(bot, message):
    await bot.send_message(message.from_user.id, "Панель администратора",
                           reply_markup=getCmdAdminButtons())

async def getSpheresResendMessage(callback_query):
    await callback_query.message.edit_text("Выберите сферу")
    await callback_query.message.edit_reply_markup(reply_markup=getSpheresButtons())

async def getSearchSurnameResendMessage(callback_query):
    await callback_query.message.edit_text("Введите фамилию: ")
    await callback_query.message.edit_reply_markup(reply_markup=getSearchButtons())

async def getSearchTagResendMessage(callback_query):
    await callback_query.message.edit_text("Введите ник(tg) в формате @user: ")
    await callback_query.message.edit_reply_markup(reply_markup=getSearchButtons())

async def getEventsResendMessage(bot, callback_query):
    await callback_query.message.edit_text("Дождитесь отправки фото")
    await callback_query.message.edit_reply_markup(reply_markup=getEventsButtons())

    media = types.MediaGroup()
    data = getEvents()

    for x in data.keys():
        try:
            media.attach_photo(types.InputFile(data[x]['path']), data[x]['description'])
        except Exception:
            pass
    try:
        await bot.send_media_group(callback_query.from_user.id, media=media)
    except exceptions.BadRequest as e:
        await errorMessage(bot, callback_query, f'{e} (Обнаружено неизвестное расширение файла)')
    except exceptions.ValidationError as e:
        await bot.send_message(callback_query.from_user.id, "Пусто")

async def getPeoplesEditMessage(bot, callback_query):
    await callback_query.message.edit_text("Измените файл и отправьте его следующим сообщением боту\n<b>Важно! Если в файле будут присутсвовать одинаковые имена, то сохранится только последнее со всеми его свойсьтвами</b>", parse_mode = types.ParseMode.HTML)
    await bot.send_document(callback_query.from_user.id, open(config.PEOPLES_PATH.get_secret_value(), 'rb'))

async def getCmdNoAdminMessage(bot, message):
    await bot.send_message(message.from_user.id, "Вы не администратор")

async def successfulyEditedMessage(bot, message):
    await bot.send_message(message.from_user.id, "Успешно", reply_markup=getSuccessfulyEditedButtons())

async def getBackToAdminPanelMessage(callback_query):
    await callback_query.message.edit_text("Панель администратора", parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getCmdAdminButtons())

async def errorEditedMessage(bot, message, error):
    await bot.send_message(message.from_user.id, f"<b>{error}</b>\nПопробуйте другой файл", parse_mode = types.ParseMode.HTML)

async def errorSendingFileMessage(bot, message):
    await bot.send_message(message.from_user.id, "Для отправки файла зайдите в соответствующий пункт")

async def errorMessage(bot, message, error):
    await bot.send_message(message.from_user.id, f"<b>Ошибка:</b> {error}", parse_mode = types.ParseMode.HTML)

async def blockMessage(bot, message):
    await bot.send_message(message.from_user.id, f"<b>У вас нет прав доступа, обратитесь к администраторам</b>", parse_mode = types.ParseMode.HTML)

async def getOneSphereMessage(callback_query, sphere):
    setSphere(callback_query.from_user.id, sphere)
    await callback_query.message.edit_text("Выберите человека", parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getOneSphereButtons(sphere))

async def getContactResendMessage(callback_query, surname):
    peoples = getPeoples()
    name = peoples[surname]['name']
    patronymic = peoples[surname]['patronymic']
    phone = peoples[surname]['phone']
    email = peoples[surname]['email']
    tg = peoples[surname]['tg']
    sphere = peoples[surname]['sphere']
    business = peoples[surname]['business']
    position = peoples[surname]['position']
    text_content = f"<b>ФИО:</b> {surname} {name} {patronymic}\n\n"

    if phone != "":
        text_content += f"<b>Телефон:</b> {phone}\n\n"

    if email != "":
        text_content += f"<b>E-mail:</b> {email}\n\n"

    if tg != "":
        text_content += f"<b>TG:</b> {tg}\n\n"

    if sphere != []:
        text_content += f"<b>Сфера(-ы):</b> {', '.join(sphere)}\n\n"

    if business != "":
        text_content += f"<b>Бизнес:</b> {business}\n\n"

    if position != "":
        text_content += f"<b>Должность:</b> {position}"

    await callback_query.message.edit_text(text_content, parse_mode = types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getContactResendButtons(getSphere(callback_query.from_user.id)))

async def errorSendingTextMessage(bot, message):
    await bot.send_message(message.from_user.id, "Для отправки текста зайдите в соответствующий пункт")

async def getContactSurnameMessage(bot, message, surname):
    if surname in getPeoples().keys():
        peoples = getPeoples()
        name = peoples[surname]['name']
        patronymic = peoples[surname]['patronymic']
        phone = peoples[surname]['phone']
        email = peoples[surname]['email']
        tg = peoples[surname]['tg']
        sphere = peoples[surname]['sphere']
        business = peoples[surname]['business']
        position = peoples[surname]['position']
        text_content = f"<b>ФИО:</b> {surname} {name} {patronymic}\n\n"

        if phone != "":
            text_content += f"<b>Телефон:</b> {phone}\n\n"

        if email != "":
            text_content += f"<b>E-mail:</b> {email}\n\n"

        if tg != "":
            text_content += f"<b>TG:</b> {tg}\n\n"

        if sphere != []:
            text_content += f"<b>Сфера(-ы):</b> {', '.join(sphere)}\n\n"

        if business != "":
            text_content += f"<b>Бизнес:</b> {business}\n\n"

        if position != "":
            text_content += f"<b>Должность:</b> {position}"

        await bot.send_message(message.from_user.id, text_content, parse_mode = types.ParseMode.HTML, reply_markup=getContactButtons())
        setState(message.from_user.id, "main")
    else:
        await bot.send_message(message.from_user.id, "Такой человек не найден", reply_markup=getContactButtons())

async def getContactTagMessage(bot, message, tag):
    peoples = getPeoples()
    surname = ""

    for x in peoples.keys():
        if peoples[x]['tg'] == tag:
            surname = x
            break

    if surname in peoples.keys():
        name = peoples[surname]['name']
        patronymic = peoples[surname]['patronymic']
        phone = peoples[surname]['phone']
        email = peoples[surname]['email']
        tg = peoples[surname]['tg']
        sphere = peoples[surname]['sphere']
        business = peoples[surname]['business']
        position = peoples[surname]['position']
        text_content = f"<b>ФИО:</b> {surname} {name} {patronymic}\n\n"

        if phone != "":
            text_content += f"<b>Телефон:</b> {phone}\n\n"

        if email != "":
            text_content += f"<b>E-mail:</b> {email}\n\n"

        if tg != "":
            text_content += f"<b>TG:</b> {tg}\n\n"

        if sphere != []:
            text_content += f"<b>Сфера(-ы):</b> {', '.join(sphere)}\n\n"

        if business != "":
            text_content += f"<b>Бизнес:</b> {business}\n\n"

        if position != "":
            text_content += f"<b>Должность:</b> {position}"

        await bot.send_message(message.from_user.id, text_content, parse_mode = types.ParseMode.HTML, reply_markup=getContactButtons())
        setState(message.from_user.id, "main")
    else:
        await bot.send_message(message.from_user.id, "Такой человек не найден", reply_markup=getContactButtons())

async def getUsersEditMessage(bot, callback_query):
    await callback_query.message.edit_text("Измените файл и отправьте его следующим сообщением боту\n<b>Важно! Если в файле будут присутсвовать одинаковые id, то сохранится только последний со всеми его свойствами</b>", parse_mode = types.ParseMode.HTML)
    await bot.send_document(callback_query.from_user.id, open(config.USERS_PATH.get_secret_value(), 'rb'))

async def getSpheresEditMessage(bot, callback_query):
    await callback_query.message.edit_text("Измените файл и отправте его следующим сообщением боту", parse_mode = types.ParseMode.HTML)
    await bot.send_document(callback_query.from_user.id, open(config.SPHERES_PATH.get_secret_value(), 'rb'))

async def getEventsEditMessage(callback_query):
    await callback_query.message.edit_text("<b>Мероприятия</b>", parse_mode=types.ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=getEventsEditButtons())

async def getEventChangeMessage(callback_query):
    await callback_query.message.edit_text(
        "Отправьте фото боту\n<b>Важно! Фото необходимо отправлять как файл</b>",
        parse_mode=types.ParseMode.HTML)

async def getEventDescriptionMessage(bot, message, num):
    await bot.send_message(message.from_user.id, "Введите описание для этого изображения", reply_markup=getEventDescription(num))

async def getSuccessfulyEditEventMessage(bot, message):
    await bot.send_message(message.from_user.id, "Успешно",
                           reply_markup=getSuccessfulyEditEventButtons())

async def errorSendingPhotoMessage(bot, message):
    await bot.send_message(message.from_user.id, "Для отправки фото зайдите в соответствующий пункт")

async def getAllMessage(bot, message, text):
    data = getUsers()
    for x in data.keys():
        if data[x]["access"] == True and x != message.from_user.id:
            await bot.send_message(x, text)

async def getSuccessfulySendAllMessage(bot, message):
    await bot.send_message(message.from_user.id, "Успешно",
                           reply_markup=getSuccessfulyEditEventButtons())