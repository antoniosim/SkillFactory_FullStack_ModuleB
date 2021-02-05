import telebot
import datetime

import extensions
import config

bot = telebot.TeleBot(config.TOKEN)
users_data = extensions.load_db(config.DB_PATH)


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    try:
        out_message = 'Привет, ' + message.from_user.first_name + '! Этот бот поможет тебе конвертировать валюты'
        bot.send_message(chat_id=message.chat.id,
                         text=out_message,
                         parse_mode='html',
                         reply_markup=extensions.button_new_query())
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) начал работу с ботом\n')
    except:
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) не смог начать работу с ботом\n')


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    try:
        out_message = message.from_user.first_name + \
                      ', для получения информации о курсах валют используй кнопки в сообщениях и следуй подсказкам!'
        bot.send_message(chat_id=message.chat.id,
                         text=out_message,
                         parse_mode='html',
                         reply_markup=extensions.button_new_query())
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) попросил помощи\n')
    except:
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) не добился помощи от бота\n')


# формирование нового запроса
@bot.message_handler(commands=['values'])
def help_message(message: telebot.types.Message):
    try:
        users_data[message.from_user.id] = extensions.UserData(message.from_user.first_name)
        extensions.save_db(config.DB_PATH, users_data)
        user_data = users_data[message.from_user.id]

        out_message = user_data.name + ', необходимо выбрать исходную валюту для конвертации'
        bot.send_message(chat_id=message.chat.id,
                         text=out_message,
                         parse_mode='html',
                         reply_markup=user_data.buttons_currency(True))
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) запросил список валют\n')
    except:
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) сумел сломать API бота\n')


@bot.callback_query_handler(lambda query: query.data == "NEW")
def process_callback_new(query: telebot.types.CallbackQuery):
    try:
        users_data[query.from_user.id] = extensions.UserData(query.from_user.first_name)
        extensions.save_db(config.DB_PATH, users_data)
        user_data = users_data[query.from_user.id]

        out_message = user_data.name + ', необходимо выбрать исходную валюту для конвертации'
        bot.edit_message_text(chat_id=query.message.chat.id,
                              message_id=query.message.id,
                              text=out_message,
                              parse_mode='html',
                              reply_markup=user_data.buttons_currency())
        bot.answer_callback_query(query.id, 'Данные из ЦБ РФ получены', False)
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {query.from_user.first_name} {query.from_user.last_name} '
              f'({query.from_user.username}) начал новый запрос\n')
    except:
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {query.from_user.first_name} {query.from_user.last_name} '
              f'({query.from_user.username}) сумел сломать API бота\n')


# обработка нажатия кнопки расширения списка валют
@bot.callback_query_handler(lambda query: query.data == "ALL")
def process_callback_all(query: telebot.types.CallbackQuery):
    try:
        user_data = users_data[query.from_user.id]

        out_message = user_data.name + ', необходимо выбрать исходную валюту'
        bot.edit_message_text(chat_id=query.message.chat.id,
                              message_id=query.message.id,
                              text=out_message,
                              parse_mode='html',
                              reply_markup=user_data.buttons_currency(True))
        bot.answer_callback_query(query.id, 'Выведены все валюты', False)
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {query.from_user.first_name} {query.from_user.last_name} '
              f'({query.from_user.username}) запросил все валюты\n')
    except:
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {query.from_user.first_name} {query.from_user.last_name} '
              f'({query.from_user.username}) сумел сломать API бота\n')


# обработка нажатия кнопки валюты
@bot.callback_query_handler(lambda query: query.data in config.FLAGS)
def process_callback_all(query: telebot.types.CallbackQuery):
    try:
        user_data = users_data[query.from_user.id]

        if user_data.base is None:
            user_data.base = query.data
            out_message = user_data.name
            out_message += ', теперь необходимо выбрать валюту для перевода\n'
            out_message += config.FLAGS[user_data.base]
            out_message += user_data.rates[user_data.base]["Name"]

            bot.edit_message_text(chat_id=query.message.chat.id,
                                  message_id=query.message.id,
                                  text=out_message,
                                  parse_mode='html',
                                  reply_markup=user_data.buttons_currency(True))
            bot.answer_callback_query(query.id,
                                      'Выбрана валюта ' + config.FLAGS[user_data.base] + ' ' +
                                      user_data.rates[user_data.base]["Name"], False)
            print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
                  f'Пользователь {query.from_user.first_name} {query.from_user.last_name} '
                  f'({query.from_user.username}) выбрал для обмена валюту {user_data.base}\n')
        elif user_data.quote is None:
            user_data.quote = query.data
            out_message = user_data.name
            out_message += ', мы будем переводить:\n\n'
            out_message += config.FLAGS[user_data.base]
            out_message += user_data.rates[user_data.base]["Name"]
            out_message += '\n' + chr(11015) + '\n'
            out_message += config.FLAGS[user_data.quote]
            out_message += user_data.rates[user_data.quote]["Name"]
            out_message += '\n\nСколько единиц валюты нужно перевести?\nВведите количество единиц (разделитель - ".")'

            bot.edit_message_text(chat_id=query.message.chat.id,
                                  message_id=query.message.id,
                                  text=out_message,
                                  parse_mode='html')

            bot.answer_callback_query(query.id,
                                      'Выбрана валюта ' + config.FLAGS[user_data.quote] + ' ' +
                                      user_data.rates[user_data.quote]["Name"], False)

            print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
                  f'Пользователь {query.from_user.first_name} {query.from_user.last_name} '
                  f'({query.from_user.username}) выбрал на обмен валюту {user_data.quote}\n')
        else:
            bot.send_message(chat_id=query.message.chat.id,
                             text='Неизвестный запрос',
                             parse_mode='html')
        extensions.save_db(config.DB_PATH, users_data)
    except:
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {query.from_user.first_name} {query.from_user.last_name} '
              f'({query.from_user.username}) сумел сломать API бота\n')


# обработка ввода текста (исключения для всего кроме чисел после запроса количества валюты)
@bot.message_handler(content_types=['text'])
def text_message(message: telebot.types.Message):
    try:
        rm = None
        try:
            user_data = users_data[message.from_user.id]
        except KeyError:
            rm = extensions.button_new_query()
            print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
                  f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
                  f'({message.from_user.username}) направлен в начало запроса\n')
            raise extensions.APIException(
                chr(9888) + chr(9888) + chr(9888) + chr(9888) + chr(9888) + \
                '\n' + message.from_user.first_name + ', не могу найти начало твоего запроса\n\n'
                                                      'Лучше начать сначала!\n\n'
                                                      'Для получения информации о курсах валют'
                                                      ' используй кнопки в сообщениях и следуй подсказкам!'
            )

        # ЕСЛИ СООБЩЕНИЕ НАПИСАНО НЕ В МОМЕНТ ЗАПРОСА КОЛИЧЕСТВА ВАЛЮТЫ
        if user_data.base is None or user_data.quote is None:
            rm = extensions.button_new_query()
            print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
                  f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
                  f'({message.from_user.username}) пытается общаться с ботом сообщениями\n')
            raise extensions.APIException(
                chr(9888) + chr(9888) + chr(9888) + chr(9888) + chr(9888) + \
                '\n' + message.from_user.first_name + ', нужно писать только тогда, когда нужно!\n\n' + \
                'Для получения информации о курсах валют используй кнопки в сообщениях и следуй подсказкам!'
            )

        # ЕСЛИ СООБЩЕНИЕ НЕ МОЖЕТ БЫТЬ ПРЕОБРАЗОВАНО В ЧИСЛО
        if not str(message.text).replace('.', '', 1).isdigit():
            rm = None
            print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
                  f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
                  f'({message.from_user.username}) затупил при вводе числа\n')
            raise extensions.APIException(
                chr(9940) + chr(9940) + chr(9940) + chr(9940) + chr(9940) + \
                '\n' + message.from_user.first_name + ', ты же понимаешь, что надо писать цифры'
            )

        user_data.amount = float(message.text)

        user_data.result = user_data.get_prices()
        out_message = chr(128176) + chr(128176) + chr(128176) + chr(128176) + chr(128176)
        out_message += '\n' + user_data.name + ', мы всё узнали:\n\n'
        out_message += chr(128197) + ' По состоянию на ' + user_data.timestamp + '\n\n'
        out_message += config.FLAGS[user_data.base] + f' {"%.2f" % user_data.amount} '
        out_message += user_data.rates[user_data.base]['Name'] + '\n'
        out_message += chr(11015) + '\n'
        out_message += config.FLAGS[user_data.quote] + f' {"%.2f" % user_data.result} '
        out_message += user_data.rates[user_data.quote]['Name'] + '\n'
        users_data.pop(message.from_user.id)
        extensions.save_db(config.DB_PATH, users_data)
        rm = extensions.button_new_query()
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) перевёл '
              f'{"%.2f" % user_data.amount}{user_data.base} в {"%.2f" % user_data.result}{user_data.quote}\n')

    except extensions.APIException as e:
        out_message = e

    except:
        out_message = chr(9940) + chr(9940) + chr(9940) + chr(9940) + chr(9940) + \
                      '\n' + message.from_user.first_name + ', что-то пошло не так\n\n' + \
                      'Для получения информации о курсах валют используй кнопки в сообщениях и следуй подсказкам!'
        users_data.pop(message.from_user.id)
        extensions.save_db(config.DB_PATH, users_data)
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) сумел сломать API бота\n')

    bot.send_message(chat_id=message.chat.id,
                     text=out_message,
                     parse_mode='html',
                     reply_markup=rm)


# обработка ввода текста (исключения для всего кроме чисел после запроса количества валюты)
@bot.message_handler(
    content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def non_text_message(message: telebot.types.Message):
    try:
        out_message = chr(9888) + chr(9888) + chr(9888) + chr(9888) + chr(9888)
        out_message += '\n' + message.from_user.first_name + ', я не знаю, зачем ты мне это присылаешь!\n\n'
        out_message += 'Для получения информации о курсах валют используй кнопки в сообщениях и следуй подсказкам!'
        rm = extensions.button_new_query()
        bot.send_message(chat_id=message.chat.id,
                         text=out_message,
                         parse_mode='html',
                         reply_markup=rm)
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) присылает какую-то ерунду\n')
    except:
        print(f'{datetime.datetime.utcnow().strftime("%d.%m.%Y %H:%M:%S")} === '
              f'Пользователь {message.from_user.first_name} {message.from_user.last_name} '
              f'({message.from_user.username}) сумел сломать API бота\n')


bot.polling()
