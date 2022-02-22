import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
import telegram  # from telegram import InlineQueryResultPhoto
from telethon import TelegramClient
import ast
from uuid import uuid4
import datetime
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import timedelta
import os
import base64
import requests
import markup
import db_cmd
import json
from settings import token, imgBB_key, provider_token#, entity, api_id, api_fash, bot_user_name

bot = telebot.TeleBot(token)
#client = TelegramClient(entity, api_id, api_fash)
scopes = ['https://www.googleapis.com/auth/calendar']
credentials = pickle.load(open('token.pkl', 'rb'))
service = build('calendar', 'v3', credentials=credentials)
# BAACAgIAAxkBAAMTYhPvoi63t-TUXNMiZfOAAyYwBdUAAisWAAK1bKBIgtnl4XS_MvojBA
# oc3elh5mfajsut5ni69u25v99o@group.calendar.google.com

# __________________StartMenu____________________
@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        db_cmd.check_user_id(uid)
        db_cmd.up_user_state(uid, 'start')
        bot.send_message(cid, "Приветствую в Yoga_bot", reply_markup=markup.gen_start_markup())
    except Exception as ex:
        print('command_start:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "start")
def callback_back_btn(call):
    try:
        uid = call.from_user.id
        db_cmd.up_user_state(uid, 'start')
        bot.send_message(uid, "Приветствую в Yoga_bot", reply_markup=markup.gen_start_markup())
    except Exception as ex:
        print('callback_back_btn:', ex)
# __________________StartMenu_end____________________

# __________________UploadVideo____________________
# async def upload_video(files):
#     path = files
#     async with client.action(bot_user_name, "document") as action:
#         await client.send_file(bot_user_name, path, progress_callback=action.progress)
#
# @bot.message_handler(content_types=['video'])
# def add_video(message):
#     cid = message.chat.id
#     uid = message.from_user.id
#     if cid==uid:
#         print('message', message)
#
#
# __________________UploadVideo_end_________________


# __________________ADMIN______________________
@bot.message_handler(commands=['admin'])
def command_admin(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if cid==uid and db_cmd.check_user_is_admin(uid):
            bot.send_message(cid, "Меню администратора\n\nПоложит новое видео в папку Video и нажмите кнопку добавить",
                             reply_markup=markup.gen_admin_markup())
        elif cid == uid and not db_cmd.check_user_is_admin(uid):
            bot.send_message(cid, "Права администратора отсутствуют\nНажмите /start для продолжения")
    except Exception as ex:
        print('start_msg:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "admin")
def callback_main_menu(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        if cid==uid and db_cmd.check_user_is_admin(uid):
            bot.send_message(cid, "Меню администратора", reply_markup=markup.gen_admin_markup())
    except Exception as ex:
        print('callback_main_menu:', ex)

# @bot.callback_query_handler(func=lambda call: call.data == "add")
# def callback_main_menu(call):
#     try:
#         cid = call.message.chat.id
#         uid = call.from_user.id
#         if cid==uid and db_cmd.check_user_is_admin(uid):
#             list_dir = os.listdir(path="./Video/")
#             list_lessons = list(map(lambda x : x[0], db_cmd.get_lessons_files_names()))
#             print(list_dir)
#             print(list_lessons)
#             for i in range(len(list_dir)):
#                 if list_dir[i] not in list_lessons:
#                     path = f'./Video/{list_dir[i]}'
#                     with client:
#                         client.loop.run_until_complete(upload_video(path))
#             bot.send_message(cid, "Меню администратора(видео добавилось)", reply_markup=markup.gen_admin_markup())
#     except Exception as ex:
#         print('callback_main_menu:', ex)




# __________________ADMIN_end__________________


# __________________UserMenu____________________
@bot.callback_query_handler(func=lambda call: call.data == "lessons")
def callback_lessons(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        if cid == uid:
            data = db_cmd.get_data(uid)
            data = dict(ast.literal_eval(data))
            if data['paid'] == 'True':
                bot.send_message(cid, "Просмотр уроков",
                                 reply_markup=markup.gen_show_lessons_markup())
            else:
                bot.send_message(cid, "Внимане\nплатный контент",
                                 reply_markup=markup.gen_lessons_not_paid_markup())
    except Exception as ex:
        print('callback_lessons:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith('video'))
def callback_video(call):
    try:
        uid = call.from_user.id
        video_id = call.data.split('_')[1]
        videofile_id = db_cmd.get_videofile_id(video_id)
        bot.send_video(uid, videofile_id)
    except Exception as ex:
        print('callback_video:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "timetable")
def callback_timetable(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        if cid == uid:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId='oc3elh5mfajsut5ni69u25v99o@group.calendar.google.com',
                                      timeMin=now,
                                      maxResults=10,
                                      singleEvents=True,
                                      orderBy='startTime').execute()
            events = events_result.get('items', [])
            message_text = ''
            for i in range(len(events)):
                message_text = message_text + f'{i+1}. {events[i]["summary"]} - {events[i]["start"]["dateTime"]}' + '\n'
            bot.send_message(cid, text="Расписание уроков")
            bot.send_message(cid, text=message_text)
    except Exception as ex:
        print('callback_timetable:', ex)



# _________________UserMenu_End________________

######



# _________________InlineQuery_________________
@bot.inline_handler(func=lambda query: types.InlineQuery)
def query_lessons(inline_query):
    try:
        uid = inline_query.from_user.id
        data = db_cmd.get_courses()
        lst_inline = []
        db_cmd.up_user_state(uid, 'inline')
        for i in data:
            video_id = i[0]
            text = f'Урок № {i[0]}'
            r = types.InlineQueryResultArticle(
                id=str(uuid4()),
                title=text,
                description='description',
                thumb_url='https://i.ibb.co/7b4hG2S/yoga.jpg',
                input_message_content=types.InputTextMessageContent(
                    message_text=f"{text} - message_text", parse_mode=''),
                reply_markup=markup.gen_watch_video_markup(video_id)
            )
            lst_inline.append(r)
        bot.answer_inline_query(inline_query.id, lst_inline, 0, switch_pm_parameter='start')
        # bot.send_video()
    except Exception as ex:
        print('query_lessons:', ex)
# __________________InlineQuery_end____________


# __________________Payment____________________
@bot.callback_query_handler(func=lambda call: call.data == "payment")
def callback_pay(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        amount = 999  # int(call.data[4:])
        db_cmd.up_user_state(uid, "pay")
        prices = [LabeledPrice(label="Оплата уроков йоги\n'LabeledPrice(label='", amount=int(amount) * 100)]
        # LabeledPrice('Доставка', 5000)]
        bot.send_invoice(cid, title='Видеоуроки йоги',
                         description='Йога - это свет, который, если зажегся однажды, никогда не погаснет. Чем лучше практика, тем ярче пламя',
                         provider_token=provider_token,
                         currency='UAH',
                         photo_url='https://i.ibb.co/7b4hG2S/yoga.jpg',
                         photo_height=512,
                         photo_width=512,
                         photo_size=512,
                         is_flexible=False,
                         prices=prices,
                         start_parameter='start',
                         invoice_payload='H')
    except Exception as ex:
        print('callback_pay:', ex)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Инопланетяне пытались украсть CVV вашей карты, но мы успешно защитили ваши учетные данные")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    cid = message.chat.id
    uid = message.from_user.id
    state = db_cmd.get_user_state(uid)
    if state == "pay":
        bot.send_message(cid, 'Оплата успешна Сумма: {} {}'.format(message.successful_payment.total_amount / 100,
                                                                   message.successful_payment.currency),
                         parse_mode="Markdown")
        bot.send_message(cid, "Учетная запись активирована")
        db_cmd.up_user_state(uid, 'start')
        data = db_cmd.get_data(uid)
        new_data = dict(ast.literal_eval(data))
        new_data['paid'] = "True"
        db_cmd.up_data(uid, str(new_data))
        bot.send_message(cid, "Приветствую в Yoga_bot", reply_markup=markup.gen_start_markup())
# __________________Payment_end____________________


# bot.skip_pending = True
# bot.polling(non_stop=True, interval=0)

while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as ex:
        print('Main Bot:', ex)
    now = datetime.datetime.utcnow().isoformat() + 'Z'

