import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import Updater, CallbackQueryHandler
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from bot.constants import START_TEXT, INVALID_COMMAND, CHOOSE_SUBJECT, INSTRUCTION, GIVE_TASK, SET_SUBJECT
from task.task import Task
from task.task_manager import TaskManager
from keys import TG_BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class TGBot:
    def __init__(self):
        self.task_manager = TaskManager()
        self.updater = Updater(token=TG_BOT_TOKEN, use_context=True)
        self.add_handlers()

    def add_handlers(self):
        self.updater.dispatcher.add_handler(CommandHandler('givetask', self.give_task))
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        self.updater.dispatcher.add_handler(CommandHandler('setsubject', self.set_subject))
        self.updater.dispatcher.add_handler(CommandHandler('setlevel', self.set_level))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.all, self.button_messages_handler))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_query_handler))

    def start(self, update: telegram.update, context):
        self.task_manager.register_new_user(update.effective_chat.id)

        custom_keyboard = [[KeyboardButton(GIVE_TASK), KeyboardButton(SET_SUBJECT)]]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=START_TEXT,
                                 reply_markup=reply_markup)

    def give_task(self, update, context):
        try:
            task_statement, task_id = self.task_manager.get_task(update.effective_chat.id)
        except KeyError as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))
            return
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Подсказка',
                                                                   callback_data=('Подсказка' + '&' + str(task_id))),
                                              InlineKeyboardButton('Решение',
                                                                   callback_data=('Решение' + '&' + str(task_id)))]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=task_statement, reply_markup=reply_markup)

    def callback_query_handler(self, update, context):
        # Handles inline buttons pressing
        query: CallbackQuery = update.callback_query

        query.answer()

        user_id = query.from_user.id
        query_type, task_id = query.data.split('&')
        if query_type == 'Подсказка':
            context.bot.send_message(chat_id=user_id,
                                     text=f'Подсказка: {self.task_manager.get_hint(user_id, int(task_id))}')
        elif query_type == 'Решение':
            context.bot.send_message(chat_id=user_id,
                                     text=f'Решение: {self.task_manager.get_solution(user_id, int(task_id))}')
        elif query_type in Task.get_subjects_list():
            self.task_manager.set_subject(user_id, query_type)
            context.bot.send_message(chat_id=user_id,
                                     text=f'Установлена тема {query_type}')

    def button_messages_handler(self, update, context):
        message_text = update.message.text
        print(f'message_text: {message_text}')
        if message_text == GIVE_TASK:
            self.give_task(update, context)
        elif message_text == SET_SUBJECT:
            self.set_subject(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=INVALID_COMMAND)

    def set_subject(self, update: telegram.update, context):
        keyboard = []
        for subject in Task.get_subjects_list():
            keyboard.append(InlineKeyboardButton(subject, callback_data=(subject + '&')))
        # TODO: generalize
        reply_markup = InlineKeyboardMarkup([keyboard[:3], keyboard[3:]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=CHOOSE_SUBJECT,
                                 reply_markup=reply_markup)

    def set_level(self, update: telegram.update, context):
        ...

    def help(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=INSTRUCTION)

    def run(self):
        self.updater.start_polling()
