import telebot
from telebot import apihelper
from package import parser

apihelper.proxy = {'https':'https://142.93.117.211:3128'}
token = '1157438899:AAGO5VIRkmrT--2-aDDPVIk3DThtE-rr3Og'

bot = telebot.TeleBot(token=token)
go = True

@bot.message_handler(commands=['start', 'help'])
def start(message):
	while go:
		if parser.comparison() == 0:
			bot.send_message('Вы приобрели новую вещь')
		else: pass


bot.polling()








