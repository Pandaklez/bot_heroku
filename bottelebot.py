import telebot
import conf #must be in the same folder with conf.py
import flask

WEBHOOK_BASE = "https://{}.{}".format(conf.WEBHOOK_HOST,conf.WEBHOOK_PORT)

WEBHOOK_URL = "/{}/".format(conf.TOKEN)

app = flask.Flask(__name__)

@app.route('/')
def index():
    return 'ok'

#conf.TOKEN #check if we can get token from file
bot = telebot.TeleBot(conf.TOKEN, threaded=False)

bot.remove_webhook()

bot.set_webhook(url = WEBHOOK_BASE + WEBHOOK_URL)

@bot.message_handler(commands = ['start', 'help'])
def welcome(message):
    reply = ''
    #code generating bot's reply to the message
    bot.send_message(message.chat.id, 'Hi bro ;)')

@bot.message_handler(func = lambda m: True)
def len_message(message):
    bot.send_message(message.chat.id, 'In your message {} symbols'.format(len(message.text)))

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм 
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
        
#if __name__ == '__main__':
#    bot.polling(none_stop=True)

#go to python anywhere. go to bash
#we should install modules in bash

