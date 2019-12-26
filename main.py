import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import time
from nredarwin.webservice import DarwinLdbSession
from datetime import datetime


def get_times(station='GVH'):
    list_ = []
    darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", 
                               api_key="##")
    board = darwin_sesh.get_station_board(station)
    for item in board.train_services:
        list_.append(f"Platform : {item.platform}| Arr: {item.std} - Exp :{item.etd} - Dest :{item.destination_text}")
    return list_
   

def webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        # Reply with the same message
        bot.sendMessage(chat_id=chat_id, text=update.message.text)
    return "ok"


    

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!, if you would like to get the train times type: trains')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    update.message.reply_text('This is training bot.. WIP @Umar RDS')

def train(update,context):
    """ask for station"""
    update.message.reply_text('What Station would you like times for ?')
    # list_ = get_times()
    y = update.message.text
    print(y)
    update.message.reply_text('Getting Times for Gravely Hill, Erdington.')
    for i in range(0,15):
        x = (f"Platform : {datetime.now().strftime('%H:%M:%S')}| Arr: {datetime.now().strftime('%H:%M:%S')} - Exp :{datetime.now().strftime('%H:%M:%S')} - Dest :{datetime.now().strftime('%H:%M:%S')}")
        update.message.reply_text(x)
        time.sleep(0.5)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("##", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("train", train))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()