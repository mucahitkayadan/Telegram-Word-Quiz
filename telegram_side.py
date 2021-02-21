# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 20:52:33 2021

@author: muham
"""
import question_answer as qa
import logging

from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


Q = qa.Question()

class Telegram(object):    
    #questions = Q.options
    #number = Q.ask.number
    
    def __init__(self):        
        self.selected_language = -1
        self.selected_option = 0
        self.updater = Updater("1606960702:AAG8xcMPMWlycUjj-FQrU0uXvNhNOfwt2to")
        self.dispatcher = self.updater.dispatcher
        Telegram.run(self)
              
    def start(self, update: Update, context: CallbackContext) -> None:
        """Inform user about what this bot can do"""
        update.message.reply_text(
            'Please select /start to select language, /quiz to get a Quiz or /preview'
            ' to generate a preview for your quiz'
        )
        #Q.checkAnswer(receive_poll_answer.selected_option, Q.langs[0], Q.langs[1])
        #receive_quiz_answer(update, context)
        
    def selectLanguagePoll(self, update: Update, context: CallbackContext) -> None:
        Telegram.start(self, update, context)
        questions = ["English to Italian", "Italian to English"]
        message = context.bot.send_poll(
            update.effective_chat.id,
            "Choose a test Method",
            questions,
            is_anonymous=False,
            allows_multiple_answers=False,
        )
        payload = {        
            message.poll.id: {
                "questions": questions,
                "message_id": message.message_id,
                "chat_id": update.effective_chat.id,
                "answers": 0, #burası sıfırdı
            }
        }
        context.bot_data.update(payload)
        
    
    def receive_language_poll_answer(self, update: Update, context: CallbackContext) -> None:
        answer = update.poll_answer 
        #print(answer)
        poll_id = answer.poll_id
        
        try:
            questions = context.bot_data[poll_id]["questions"]
        except KeyError:
            return
        
        self.selected_language = int(answer.option_ids[0]) 
        print("selected_language = " + str(self.selected_language) + "\n")
        answer_string = str(questions[int(self.selected_language)])
        context.bot.send_message(
            context.bot_data[poll_id]["chat_id"],
            f"{update.effective_user.mention_html()} selected {answer_string}!",
            parse_mode=ParseMode.HTML,
        )
        payload = {        
            answer.poll_id: {
                "answers": self.selected_language, #burası sıfırdı
            }
        }
        context.bot_data.update(payload)  
             
    
    
        
    def quiz(self, update: Update, context: CallbackContext) -> None:
        """Send a predefined poll"""
        #questions = ["1", "2", "4", "20"]
        questions = qa.Question().options
        message = update.effective_message.reply_poll(
            "How many eggs do you need for a cake?", questions, type=Poll.QUIZ, correct_option_id=2
        )
        # Save some info about the poll the bot_data for later use in receive_quiz_answer
        payload = {
            message.poll.id: {
                "questions": questions,
                "chat_id": update.effective_chat.id, 
                "message_id": message.message_id}
        }
        context.bot_data.update(payload)
    
    
    def receive_quiz_answer(self, update: Update, context: CallbackContext) -> None:
        answer = update.poll_answer    
        poll_id = answer.poll_id
        
        try:
            questions = context.bot_data[poll_id]["questions"]
        except KeyError:
            return
        
        selected_option = answer.option_ids[0]    
        answer_string = str(questions[int(selected_option)])
        context.bot.send_message(
            context.bot_data[poll_id]["chat_id"],
            f"{update.effective_user.mention_html()} selected {answer_string}!",
            parse_mode=ParseMode.HTML,
        )
    
    def preview(self, update: Update, context: CallbackContext) -> None:
        """Ask user to create a poll and display a preview of it"""
        # using this without a type lets the user chooses what he wants (quiz or poll)
        button = [[KeyboardButton("Press me!", request_poll=KeyboardButtonPollType())]]
        message = "Press the button to let the bot generate a preview for your poll"
        # using one_time_keyboard to hide the keyboard
        update.effective_message.reply_text(
            message, reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
        )
    
    
    def receive_poll(self, update: Update, context: CallbackContext) -> None:
        """On receiving polls, reply to it by a closed poll copying the received poll"""
        actual_poll = update.effective_message.poll
        # Only need to set the question and options, since all other parameters don't matter for
        # a closed poll
        update.effective_message.reply_poll(
            question=actual_poll.question,
            options=[o.text for o in actual_poll.options],
            # with is_closed true, the poll/quiz is immediately closed
            is_closed=True,
            reply_markup=ReplyKeyboardRemove(),
        )
    
    
    def help_handler(self, update: Update, context: CallbackContext) -> None:
        """Display a help message"""
        update.message.reply_text("Use /quiz, /start or /preview to test this " "bot.")
    
    
    def run(self) -> None:
    
        self.dispatcher.add_handler(CommandHandler('start', self.selectLanguagePoll))
        self.dispatcher.add_handler(PollAnswerHandler(self.receive_language_poll_answer))
        print("selected_language = " + str(self.selected_language) + "\n")
        Q.selectLang(self.selected_language+1) 
        Q.ask(Q.langs[0], Q.langs[1])
        self.dispatcher.add_handler(CommandHandler('quiz', self.quiz))
        self.dispatcher.add_handler(PollAnswerHandler(self.receive_quiz_answer))    
        self.dispatcher.add_handler(CommandHandler('preview', self.preview))
        self.dispatcher.add_handler(MessageHandler(Filters.poll, self.receive_poll))
        self.dispatcher.add_handler(CommandHandler('help', self.help_handler))
    
        # Start the Bot
        self.updater.start_polling()
    
        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        self.updater.idle()

Telegram()    
# if __name__ == '__main__':
    
#     run()