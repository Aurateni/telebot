import telebot
import json


TOKEN = '305043240:AAHOkqOAmG0-LGVNws0rVobg7fsz8zy7HJo'

START_ADD, LOCATION = range(2)
bot = telebot.TeleBot(TOKEN)


def get_state(message):
    locations = []
    with open('data.json', 'r') as f:
        locations = json.load(f)
    for item in locations:
        if item["id"] == message.chat.id:
            return item["state"]
    else:
        locations.append(
            {
                "id": message.chat.id,
                "state": 0,
                "list": []
            }
        )
        with open('data.json', 'w') as f:
            json.dump(locations, f)
        return 0


def update_state(message, state):
    locations = []
    with open('data.json', 'r') as f:
        locations = json.load(f)
    for item in locations:
        if item["id"] == message.chat.id:
            item["state"] = state
    with open('data.json', 'w') as f:
        json.dump(locations, f)


def get_locations(user_id):
    locations = []
    with open('data.json', 'r') as f:
        locations = json.load(f)
    for item in locations:
        if item["id"] == user_id:
            list_text = ''
            for i in item["list"][::-1][0:10]:
                list_text = list_text + ''.join(i) + ';\n'
            return list_text


def add_location(user_id, value):
    locations = []
    with open('data.json', 'r') as f:
        locations = json.load(f)
    for item in locations:
        if item["id"] == user_id:
            item["list"].append(value)
    with open('data.json', 'w') as f:
        json.dump(locations, f)


def delete_locations(user_id):
    locations = []
    with open('data.json', 'r') as f:
        locations = json.load(f)
    for item in locations:
        if item["id"] == user_id:
            item["list"].clear()
    with open('data.json', 'w') as f:
        json.dump(locations, f)


@bot.message_handler(commands=['help', 'start'])
def handle_message(message):
    help_text = "/add – добавление нового места;\n\
            /list – отображение добавленных мест;\n\
            /reset позволяет пользователю удалить все его добавленные локации;\n"
    bot.send_message(chat_id=message.chat.id, text=help_text)


@bot.message_handler(commands=['add'], func=lambda message: get_state(message) == START_ADD)
def handle_add(message):
    bot.send_message(chat_id=message.chat.id, text='введите адрес:')
    update_state(message, LOCATION)


@bot.message_handler(func=lambda message: get_state(message) == LOCATION)
def handle_location(message):
    add_location(message.chat.id, message.text)
    bot.send_message(chat_id=message.chat.id, text='адрес успешно добавлен!')
    update_state(message, START_ADD)


@bot.message_handler(commands=['list'])
def handle_list(message):
    list_text = get_locations(message.chat.id)
    if list_text == '':
        bot.send_message(chat_id=message.chat.id, text='нет адресов')
    else:
        bot.send_message(chat_id=message.chat.id, text=list_text)


@bot.message_handler(commands=['reset'])
def handle_reset(message):
    delete_locations(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='все адреса удалены')


if __name__ == '__main__':
  bot.polling()
