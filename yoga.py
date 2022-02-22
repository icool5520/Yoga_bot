import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption
import telegram  # from telegram import InlineQueryResultPhoto
from telethon import TelegramClient
import ast
from uuid import uuid4
import os
import base64
import requests
import markup
import db_cmd
import json
from settings import token, imgBB_key, provider_token, entity, api_id, api_fash, bot_user_name

bot = telebot.TeleBot(token)
client = TelegramClient(entity, api_id, api_fash)
# BAACAgIAAxkBAAMTYhPvoi63t-TUXNMiZfOAAyYwBdUAAisWAAK1bKBIgtnl4XS_MvojBA

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
async def upload_video(files):
    path = files
    async with client.action(bot_user_name, "document") as action:
        await client.send_file(bot_user_name, path, progress_callback=action.progress)

@bot.message_handler(content_types=['video'])
def add_video(message):
    cid = message.chat.id
    uid = message.from_user.id
    if cid==uid:
        print('message', message)


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

@bot.callback_query_handler(func=lambda call: call.data == "add")
def callback_main_menu(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        if cid==uid and db_cmd.check_user_is_admin(uid):
            list_dir = os.listdir(path="./Video/")
            list_lessons = list(map(lambda x : x[0], db_cmd.get_lessons_files_names()))
            print(list_dir)
            print(list_lessons)
            for i in range(len(list_dir)):
                if list_dir[i] not in list_lessons:
                    path = f'./Video/{list_dir[i]}'
                    with client:
                        client.loop.run_until_complete(upload_video(path))
            bot.send_message(cid, "Меню администратора(видео добавилось)", reply_markup=markup.gen_admin_markup())
    except Exception as ex:
        print('callback_main_menu:', ex)




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
# _________________UserMenu_End________________


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









'''
@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        db_cmd.check_user_id(uid)
        db_cmd.up_user_state(uid, 'start')
        bot.send_message(cid, "CrypyoMonitor", reply_markup=markup.gen_markup())
    except Exception as ex:
        print('start_msg:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "start")
def back_to_start(call):
    try:
        uid = call.from_user.id
        cid = uid
        db_cmd.check_user_id(uid)
        db_cmd.up_user_state(uid, 'start')
        bot.send_message(cid, "CrypyoMonitor", reply_markup=markup.gen_markup())
    except Exception as ex:
        print('back_to_start:', ex)


@bot.inline_handler(func=lambda query: types.InlineQuery)
def query_text(inline_query):
    try:
        uid = inline_query.from_user.id
        data = db_cmd.get_coins()
        lst_inline = []
        db_cmd.up_user_state(uid, 'inline')
        for i in data:
            text = f'Название:{i[0]}\nЦена:{i[1]}\nРост:{i[2]}'
            r = types.InlineQueryResultArticle(
                id=str(uuid4()),
                title=str(i[0]),
                description=f'Цена:{i[1]}',
                thumb_url=f'{i[3]}',
                input_message_content=types.InputTextMessageContent(
                    message_text=f"{text}\n[\u00A0]({i[3]})", parse_mode='Markdown'),
                reply_markup=markup.gen_to_start_markup()
            )
            lst_inline.append(r)
        bot.answer_inline_query(inline_query.id, lst_inline, 0, switch_pm_parameter='start')
    except Exception as ex:
        print('query_text:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "add")
def callback_add_coin(call):
    try:
        uid = call.from_user.id
        db_cmd.up_user_state(uid, "add_coin")
        bot.send_message(uid, "Введите информацию о монете")

    except Exception as ex:
        print('callback_add_coin:', ex)


@bot.message_handler(func=lambda m: True)
# @bot.message_handler(content_types=['text'])
def echo_text(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if cid == uid:
            state = db_cmd.get_user_state(uid)
            if state == 'add_coin':
                global lst_text
                lst_text = message.text.split(',')
                db_cmd.up_user_state(uid, 'photo')
                bot.send_message(cid, 'Пришли logo монеты')

    except Exception as ex:
        print('echo_text:', ex)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        state = db_cmd.get_user_state(uid)
        if cid == uid:
            if state == 'photo':
                file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
                img = bot.download_file(file_info.file_path)
                src = file_info.file_path
                with open(src, 'wb') as new_file:
                    new_file.write(img)
                with open(f"photos/{src.split('/')[1]}", 'rb') as file:
                    url = 'https://api.imgbb.com/1/upload'
                    payload = {"key": imgBB_key, "image": base64.b64encode(file.read())}
                    res = requests.post(url, payload)
                    resp = res.json()
                    print(resp["data"]["url"])
                db_cmd.set_coin(lst_text[0], lst_text[1], lst_text[2], resp["data"]["url"])


    except Exception as ex:
        print('get_photo:', ex)


@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        db_cmd.check_user_id(uid)
        bot.send_message(cid, "Магазин", reply_markup=markup.gen_markup())
    except Exception as ex:
        print('start_msg:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "start")
def callback_main_menu(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        db_cmd.check_user_id(uid)
        bot.send_message(cid, "Магазин", reply_markup=markup.gen_markup())
    except Exception as ex:
        print('callback_main_menu:', ex)

@bot.message_handler(commands=['admin'])
def command_admin(message):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if cid==uid and db_cmd.check_user_is_admin(uid):
            bot.send_message(cid, "Меню администратора", reply_markup=markup.gen_admin_markup())
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def callback_categors(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            categor = str(call.data[4:])
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Продукция категории: " + str(categor),
                                  reply_markup=markup.gen_products_menu_markup(categor))
    except Exception as ex:
        print('callback_categors:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("prod_"))
def callback_products(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            id_product = int(call.data[5:])
            info = db_cmd.get_info_product(id_product)
            data = db_cmd.get_data(uid)
            new_data = dict(ast.literal_eval(data))
            new_data['id'] = id_product
            db_cmd.up_data(uid, str(new_data))
            bot.send_photo(cid, photo=info[5])
            cart_content = db_cmd.get_cart_not_confirmed(uid)
            if cart_content is None or id_product not in list(ast.literal_eval(cart_content[2])):
                bot.send_message(cid, f"Название: {info[1]}\nЦена: {info[3]}\nИнфо: {info[4]}",
                             reply_markup=markup.buy(id_product))
            else:
                lst_id_product = list(ast.literal_eval(cart_content[2]))
                num = lst_id_product.count(id_product)
                bot.send_message(cid, f"Название: {info[1]}\nЦена: {info[3]}\nИнфо: {info[4]}" +
                                 f"\n\n\U00002705Добавлено в корзину {num} - шт.", reply_markup=markup.buy(id_product))
    except Exception as ex:
        print('callback_products:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def callback_add_to_cart(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            id_product = int(call.data[4:])
            info = db_cmd.get_info_product(id_product)
            price_product = info[3]  # integer
            cart_content = db_cmd.get_cart_not_confirmed(uid)
            if cart_content is None:
                lst_id_product = []
                lst_id_product.append(id_product)
                db_cmd.set_cart(uid, str(lst_id_product), price_product)
            else:
                lst_id_product = list(ast.literal_eval(cart_content[2]))
                lst_id_product.append(id_product)
                amount = price_product + cart_content[3]
                db_cmd.up_cart(uid, str(lst_id_product), amount)
            num = lst_id_product.count(id_product)
            bot.edit_message_text(chat_id=cid, message_id=mid, text=f"Название: {info[1]}\nЦена: {info[3]}\nИнфо: {info[4]}" +
                                 f"\n\n\U00002705Добавлено в корзину - {num} шт.", reply_markup=markup.buy(id_product))
    except Exception as ex:
        print('callback_add_to_cart:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "cart")
def callback_display_cart(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            cart_content = db_cmd.get_cart_not_confirmed(uid)
            if cart_content is None:
                bot.send_message(chat_id=cid, text= "---Корзина--- ")
                bot.send_message(chat_id=cid, text="Корзина пуста", reply_markup=markup.gen_empty_markup())
            else:
                lst_id_product = list(ast.literal_eval(cart_content[2]))
                unique_list_id_product = list({key: None for key in lst_id_product}.keys())
                amount = cart_content[3]
                if len(unique_list_id_product) == 1:
                    info_product = db_cmd.get_info_product(unique_list_id_product[0])
                    bot.send_message(chat_id=cid, text=f"{info_product[1]} \nКол-во: {lst_id_product.count(int(info_product[0]))}\n" +
                                                       f"\nИтого: {amount} грн.", reply_markup=markup.gen_cart_markup(amount))
                else:
                    info_product = db_cmd.get_info_product_cart(tuple(unique_list_id_product))
                    bot.send_message(chat_id=cid, text= "---Корзина---")
                    cart_text_message = ""
                    for i in unique_list_id_product:
                        for j in info_product:
                            if int(j[0]) == i:
                                cart_text_message = cart_text_message + f"{j[1]} \nКол-во: {lst_id_product.count(int(j[0]))}\n"
                    cart_text_message = cart_text_message + f"\nИтого: {amount} грн."
                    bot.send_message(chat_id=cid, text=cart_text_message, reply_markup=markup.gen_cart_markup(amount))
    except Exception as ex:
        print('callback_display_cart:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "delete_order")
def callback_delete_order(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            db_cmd.delete_order_cart(uid)
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Заказ удалён",
                                  reply_markup=markup.gen_empty_markup())
    except Exception as ex:
        print('callback_delete_order:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "confirm_order")
def callback_confirm_order(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            db_cmd.up_cart_order_status_by_uid(uid, "confirmed")
            bot.edit_message_text(chat_id=cid, message_id=mid, text="Заказ отправлен в обаботку",
                                  reply_markup=markup.gen_empty_markup())
    except Exception as ex:
        print('callback_confirm_order:', ex)

@bot.callback_query_handler(func=lambda call: call.data == "orders")
def callback_orders(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            orders = db_cmd.get_cart_confirmed()
            print(orders)
            if len(orders) == 0:
                bot.send_message(chat_id=cid,text="Заказы отсутствуют", reply_markup=markup.gen_admin_empty_markup())
            else:
                for i in orders:
                    order_text = f"Заказ: #{i[0]}\nUser: {uid}\nНа сумму:{i[3]}"
                    bot.send_message(chat_id=cid,text=order_text, reply_markup=markup.gen_admin_order_accept_markup(i[0]))
    except Exception as ex:
        print('callback_orders:', ex)



@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_order_"))
def callback_accept_order(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            id_order = int(call.data[13:])
            order = db_cmd.get_cart_by_id(id_order)
            user_id = order[1]
            db_cmd.up_cart_order_status_by_id(id_order, "accepted")
            order_text = f"Ваш заказ #{id_order} на сумму: {order[3]}грн. принят\nОжидайте уведомление об отправке"
            bot.send_message(chat_id=user_id,text=order_text)
    except Exception as ex:
        print('callback_accept_order:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("cancel_order_"))
def callback_cancel_order(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            id_order = int(call.data[13:])
            order = db_cmd.get_cart_by_id(id_order)
            user_id = order[1]
            db_cmd.up_cart_order_status_by_id(id_order, "canceled")
            order_text = f"Ваш заказ #{id_order} на сумму: {order[3]}грн. отменен"
            bot.send_message(chat_id=user_id,text=order_text)
    except Exception as ex:
        print('callback_cancel_order:', ex)


@bot.callback_query_handler(func=lambda call: call.data == "products")
def callback_admin_menu_products(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        mid = call.message.message_id
        if cid == uid:
            bot.send_message(chat_id=cid,text="Меню товаров", reply_markup=markup.gen_admin_products_markup())
    except Exception as ex:
        print('callback_admin_menu_products:', ex)


@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def callback_pay(call):
    try:
        cid = call.message.chat.id
        uid = call.from_user.id
        amount = int(call.data[4:])
        db_cmd.up_user_state(uid, "pay")
        prices = [LabeledPrice(label="оплата товараLabeledPrice", amount=int(amount)*100),
                LabeledPrice('Доставка', 5000)]
        bot.send_invoice(cid, title='Название товара',
                        description='Описание товара',
                        provider_token=provider_token,
                        currency='uah',
                        photo_url='https://creativnost.ua/7557-thickbox_default/shtamp-spasibo-za-pokupku-43kh34-sm.jpg',
                        photo_height=512,
                        photo_width=512,
                        photo_size=512,
                        is_flexible=True,
                        prices=prices,
                        start_parameter='start',
                        invoice_payload='H')
    except Exception as ex:
        print('callback_pay:', ex)

shipping_options = [ShippingOption(id='instant', title='Доставка').add_price(
                    LabeledPrice('Новая почта', 10000)),
                    ShippingOption(id='pickup', title='Доставка по городу').add_price(
                    LabeledPrice('Курьер', 5000))]

@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    uid = shipping_query.from_user.id
    state = db_cmd.get_user_state(uid)
    if state == "pay":
        bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                                error_message='Ошибка доставки платежа')

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    cid = message.chat.id
    uid = message.from_user.id
    state = db_cmd.get_user_state(uid)
    if state == "pay":
        bot.send_message(cid, 'Оплата успешна Сумма:{}{}'.format(message.successful_payment.total_amount/100, message.successful_payment.currency),
        parse_mode="Markdown")
    # up_state_pay(uid, 'start')

'''
# bot.skip_pending = True
# bot.polling(non_stop=True, interval=0)

while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as ex:
        print('Main Bot:', ex)
