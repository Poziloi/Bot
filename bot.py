from werkzeug.security import check_password_hash

#from flask_sqlalchemy import SQLAlchemy
import telebot
#from telebot import types

from models import User
from app import db, create_app

bot = telebot.TeleBot('5410293127:AAHV0j7TsxKELoMLDFlac6SlcbwEjs6V0QI') #@proekt_perevod_bot - тег бота в телеграмм
user_id ={}

print('Бот запущен и готов к работе!')

@bot.message_handler(commands=["start", "help"])
def start(message):
        bot.send_message(message.chat.id, 'Вас приветстует бот, предназначенный для рассылки информации о созданных заданиях на платформе Taskii\nДля получения рассылки, необходимо заречестрироваться в боте, введя данные для входа с сайта.')

@bot.message_handler(commands=["registration"])
def user_registration(message):
        bot.send_message(message.chat.id, 'Введите логин и пароль от сайта в одну строку через пробел.\n')

@bot.message_handler(content_types=["text"])
def get_login(message):
        app = create_app()
        app.app_context().push()

        input_data = str(message.text)
        try:
                data = input_data.split(maxsplit = 1)
        except:
                bot.send_message(message.chat.id, f'Неверный ввод. Попробуйте снова, введя /registration')
        print(data)
        #bot.send_message(message.chat.id, f'Спасибо) Ваш логин {data[0]}. Ваш пароль {data[1]}\n')
        login = data[0]
        password = data[1]
        #print(login,'\t', password)
        if len(login)>0 and len(password)>0:
                try:
                        user = User.query.filter_by(email=login).first()
                        #print(user)
                        if (user.role == 'Преподаватель') and (check_password_hash(user.password, password)):
                                user_name = user.name
                                #print(user_name)
                                try:
                                        user_id[user_name] = message.chat.id
                                        bot.send_message(message.chat.id, f'Вы успешно зарегистрировались в боте.\nТеперь при создании задания студентом, вы будете получать сообщение.')
                                        #print(user_id)
                                except:
                                        bot.send_message(message.chat.id, 'Такой пользователь уже зарегистрирован, дуралей!')
                        else:
                                bot.send_message(message.chat.id,'Отказано в доступе.\nВведенный пользователь должен быть преподавателем')
                except:
                        bot.send_message(message.chat.id,'Пользователь не найден. Невереный логин или пароль.')

def get_task_info(user_to, user_from, title, text = None):
        global user_id
        user_f = User.query.filter_by(id=user_from).first()
        user_t = User.query.filter_by(id=user_to).first()
        bot.send_message(user_id[user_t.name], f'Пользователь {user_f.name} создал вам задачу\nТема: {title}\n{text}')#сюда еще можно добавить ссылку на созданный таск

bot.polling(none_stop=True, interval=0)