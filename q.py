import telebot
import csv
import os

bot = telebot.TeleBot("5980561295:AAH5pp5TqBI28Y-fOE9zU55CZCkmTzlGy_A")

active_users = {}

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(chat_id=message.chat.id, text='Привет! Это бот банка. Выберите действие:', reply_markup=menu_keyboard)

menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
menu_keyboard.add("Регистрация", "Вход")

bank_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
bank_keyboard.add("Курс", "Счёт", "Перевод", "Клиенты банка")

def menu(message):
    bot.send_message(chat_id=message.chat.id, text="Выберите действие", reply_markup=menu_keyboard)

def registration(message):
    bot.send_message(chat_id=message.chat.id, text="Введите логин")
    bot.register_next_step_handler(message, save_login)

def save_login(message):
    login = message.text
    if os.path.isfile("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                if line.startswith(login):
                    bot.send_message(chat_id=message.chat.id, text="Пользователь с таким логином уже зарегистрирован")
                    return
    else:
        with open("users.txt", "w") as file:
            pass

    bot.send_message(chat_id=message.chat.id, text="Введите пароль")
    bot.register_next_step_handler(message, save_password, login)

def save_password(message, login):
    password = message.text

    with open("users.txt", "a", newline='') as file:
        writer = csv.writer(file, delimiter=':')
        writer.writerow([login, password, 0])

    bot.send_message(chat_id=message.chat.id, text="Регистрация прошла успешно, что бы продолжить пользование войдите в аккаунт")

def login(message):
    bot.send_message(chat_id=message.chat.id, text="Введите логин")
    bot.register_next_step_handler(message, check_login)

def check_login(message):
    login = message.text

    if os.path.isfile("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                if line.startswith(login):
                    bot.send_message(chat_id=message.chat.id, text="Введите пароль")
                    bot.register_next_step_handler(message, check_password, login)
                    return
            bot.send_message(chat_id=message.chat.id, text="Пользователь с таким логином не зарегистрирован")
    else:
        bot.send_message(chat_id=message.chat.id, text="Пользователь с таким логином не зарегистрирован")

def check_password(message, login):
    password = message.text

    with open("users.txt", "r") as file:
        for line in file:
            if line.startswith(f"{login}:{password}"):
                active_users[message.chat.id] = login
                bot.send_message(chat_id=message.chat.id, text="Вход выполнен успешно", reply_markup=bank_keyboard)
                return

    bot.send_message(chat_id=message.chat.id, text="Неверный пароль")

def course(message):
    bot.send_message(chat_id=message.chat.id, text="Железо: 3 марки\nУголь: 1 марка\nЗолото: 2 марки\nАлмаз: 7 марок")

def balance(message):
    if message.chat.id in active_users:
        with open("users.txt", "r") as file:
            for line in file:
                if line.startswith(active_users[message.chat.id]):
                    balance = line.strip().split(":")[2]
                    bot.send_message(chat_id=message.chat.id, text=f"Ваш счёт: {balance} марок")
                    return
    else:
        bot.send_message(chat_id=message.chat.id, text="Сначала нужно выполнить вход для этого введите команду /start")

def transfer(message):
    bot.send_message(chat_id=message.chat.id, text="Введите логин получателя")
    bot.register_next_step_handler(message, check_recipient)

@bot.message_handler(func=lambda message: message.text == "Регистрация")
def handle_registration(message):
    registration(message)

@bot.message_handler(func=lambda message: message.text == "Вход")
def handle_login(message):
    login(message)

@bot.message_handler(func=lambda message: message.text == "Курс")
def handle_course(message):
    course(message)

@bot.message_handler(func=lambda message: message.text == "Счёт")
def handle_balance(message):
    balance(message)

@bot.message_handler(func=lambda message: message.text == "Клиенты банка")
def handle_clients(message):
    with open("users.txt", "r") as file:
        logins = [line.strip().split(":")[0] for line in file]
    if len(logins) == 0:
        bot.send_message(chat_id=message.chat.id, text="В базе данных нет зарегистрированных пользователей")
    else:
        bot.send_message(chat_id=message.chat.id, text="Зарегистрированные пользователи:\n" + "\n".join(logins))

def transfer(message):
    bot.send_message(chat_id=message.chat.id, text="Введите логин получателя")
    bot.register_next_step_handler(message, check_recipient)

def check_transfer_amount(message, recipient):
    try:
        transfer_amount = int(message.text)
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Сумма перевода должна быть целым числом")
        return

    if transfer_amount <= 0:
        bot.send_message(chat_id=message.chat.id, text="Сумма перевода должна быть положительным числом")
        return

    sender = active_users[message.chat.id]

    with open("users.txt", "r") as file:
        reader = csv.reader(file, delimiter=':')
        for row in reader:
            if row[0] == sender:
                sender_balance = int(row[2])
            elif row[0] == recipient:
                recipient_balance = int(row[2])

    if sender_balance < transfer_amount:
        bot.send_message(chat_id=message.chat.id, text="Недостаточно средств на счете для перевода")
        return

    with open("users.txt", "r") as file:
        lines = file.readlines()

    with open("users.txt", "w") as file:
        writer = csv.writer(file, delimiter=':')
        for line in lines:
            if line.startswith(sender):
                sender_parts = line.strip().split(":")
                sender_parts[2] = str(int(sender_parts[2]) - transfer_amount)
                line = ":".join(sender_parts) + "\n"
            elif line.startswith(recipient):
                recipient_parts = line.strip().split(":")
                recipient_parts[2] = str(int(recipient_parts[2]) + transfer_amount)
                line = ":".join(recipient_parts) + "\n"
            file.write(line)

    bot.send_message(chat_id=message.chat.id, text=f"Перевод успешно выполнен. Ваш баланс: {sender_balance - transfer_amount}")

def check_recipient(message):
    recipient = message.text

    with open("users.txt", "r") as file:
        for line in file:
            if line.startswith(recipient):
                bot.send_message(chat_id=message.chat.id, text="Введите сумму перевода")
                bot.register_next_step_handler(message, check_transfer_amount, recipient)
                return

        bot.send_message(chat_id=message.chat.id, text="Пользователь с таким логином не зарегистрирован")

def process_transfer(message, recipient):
    try:
        amount = int(message.text)
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Сумма перевода должна быть целым числом")
        return

    with open("users.txt", "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith(active_users[message.chat.id]):
            balance = int(line.strip().split(":")[2])
            if balance < amount:
                bot.send_message(chat_id=message.chat.id, text="На вашем счёте недостаточно средств для перевода")
                return
            else:
                lines[i] = f"{active_users[message.chat.id]}:{line.strip().split(':')[1]}:{balance - amount}\n"
                for j, rline in enumerate(lines):
                    if rline.startswith(recipient):
                        rlines = rline.strip().split(":")
                        rlines[2] = str(int(rlines[2]) + amount)
                        lines[j] = ":".join(rlines) + "\n"
                        with open("users.txt", "w") as file:
                            file.writelines(lines)
                        bot.send_message(chat_id=message.chat.id, text=f"Перевод в размере {amount} марок выполнен успешно")
                        return

    bot.send_message(chat_id=message.chat.id, text="Не удалось выполнить перевод")

@bot.message_handler(func=lambda message: message.text == "Перевод")
def handle_transfer(message):
    bot.send_message(chat_id=message.chat.id, text="Кому бы вы хотели сделать перевод?")
    bot.register_next_step_handler(message, check_recipient)

bot.polling(none_stop=True)