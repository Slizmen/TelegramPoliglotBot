import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import json

import random

import logging

from TOKEN import TOKEN

with open('words.json', encoding='utf-8') as file:
    words = json.load(file)

logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class Bot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Начать игру'), KeyboardButton('О боте'))
        self.count = 0

        @self.bot.message_handler(commands=['start'])
        def start(message):
            logging.info('Новый пользователь')
            self.bot.send_message(message.chat.id, '''Данный бот помогает учить английский язык.
Он выводит уровень знаний после вашего перевода данных им слов.
Проект реализовал Чукичев Константин.
            ''', reply_markup=keyboard)

        @self.bot.message_handler(regexp=r'Начать игру')
        def start_game(message):
            logging.info('Пользователь начал игру')
            question, answer = self.get_questions()
            self.bot.send_message(message.chat.id, question, reply_markup=keyboard)

        @self.bot.message_handler(regexp=r'О боте')
        def welcome(message):
            logging.info('Получена информация о боте')
            self.bot.send_message(message.chat.id, '''Данный бот помогает учить английский язык.
Он выводит уровень знаний после вашего перевода данных им слов.
Проект реализовал Чукичев Константин.
            ''', reply_markup=keyboard)

        @self.bot.message_handler(func=lambda message: True)
        def Answer(message):
            if message.text == self.true_answer:
                logging.info('Дан правильный ответ')
                self.bot.reply_to(message, 'Верно')
                self.count += 1
                question, answer = self.get_questions()
                self.bot.send_message(message.chat.id, question, reply_markup=keyboard)

            else:
                logging.info('Завершение игры')
                self.bot.reply_to(message, 'Неверно!')
                self.bot.reply_to(message, f'Правильный ответ: {self.true_answer}')
                self.bot.send_message(message.chat.id, f'Вы набрали {self.count} баллов!')
                if self.count in range(10, 50):
                    self.bot.send_message(message.chat.id, f'Ваш уровень: stupid')
                elif self.count in range(50, 100):
                    self.bot.send_message(message.chat.id, f'Ваш уровень: student')
                elif self.count in range(100, 500):
                    self.bot.send_message(message.chat.id, f'Ваш уровень: brain')
                elif self.count > 500:
                    self.bot.send_message(message.chat.id, f'Ваш уровень: mega brain')
                else:
                    self.bot.send_message(message.chat.id, f'Ваш уровень: very stupid')
                logging.info(f'Уровень пользователя {self.count}')
                self.count = 0
    
    def get_questions(self):
        logging.info('Получение нового вопроса')
        dict = random.choice(words)
        question = dict['en']
        if ', ' in dict['ru']:
            answer = dict['ru'].split(', ')[0]
        else:
            answer = dict['ru'].split()[0]
        self.true_answer = answer
        return f'Как переводится: {question}?', answer
    
    def run(self):
        self.bot.infinity_polling()
    
bot = Bot()
bot.run()

