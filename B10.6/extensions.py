import telebot
import requests
import datetime
import json
import pickle

import config


class APIException(Exception):
    pass


def load_db(filename):
    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
    except:
        data = dict()
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
    return data


def save_db(filename, data):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
            return True
    except:
        return False


class UserData:

    def __init__(self, user_name):
        data = json.loads(requests.get(config.BANK_URL).content)
        self.name = user_name
        self.base = None
        self.quote = None
        self.amount = 0
        self.result = 0
        self.timestamp = datetime.datetime. \
            strptime(data['Timestamp'][:19], "%Y-%m-%dT%H:%M:%S"). \
            strftime('%d.%m.%Y %H:%M:%S')
        self.rates = data['Valute']
        self.rates['RUR'] = {"NumCode": 810,
                             "CharCode": "RUR",
                             "Nominal": 1,
                             "Name": "Российский рубль",
                             "Value": 1}

    def get_prices(self):
        fr_rate = float(self.rates[self.base]['Value']) / float(self.rates[self.base]['Nominal'])
        to_rate = float(self.rates[self.quote]['Value']) / float(self.rates[self.quote]['Nominal'])
        return self.amount * fr_rate / to_rate

    def buttons_currency(self, show_all=False):
        markup = telebot.types.InlineKeyboardMarkup()
        buttons = list()

        for currency in config.MAIN_CURRENCIES:
            if currency != self.base:
                buttons.append(
                    telebot.types.InlineKeyboardButton(text=config.FLAGS[currency] + currency + config.FLAGS[currency],
                                                       callback_data=currency))
        markup.row(*buttons)
        buttons = list()
        if show_all:
            for currency in self.rates:
                if all([currency in config.FLAGS,
                        currency not in config.MAIN_CURRENCIES,
                        currency != self.base]):
                    buttons.append(
                        telebot.types.InlineKeyboardButton(
                            text=config.FLAGS[currency] + currency + config.FLAGS[currency],
                            callback_data=currency))
                if len(buttons) > 3:
                    markup.row(*buttons)
                    buttons = list()
            if len(buttons):
                markup.row(*buttons)
        else:
            buttons.append(
                telebot.types.InlineKeyboardButton(text=chr(128176) + ' Другие валюты ' + chr(128176),
                                                   callback_data="ALL"))
            markup.row(*buttons)
        return markup


def button_new_query():
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text=chr(127381) + ' Новая конвертация ' + chr(127381),
                                                callback_data='NEW')
    markup.row(button)

    return markup
