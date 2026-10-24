import os
import telebot
from telebot import types

# ቶከኑን ከ Render Environment Variable ያነባል
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

WEB_APP_URL = 'https://splendorous-mermaid-b768fa.netlify.app'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    web_app_btn = types.InlineKeyboardButton(
        text="🚗 SchoolBus ET ሚኒ አፕ", 
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    
    markup.add(web_app_btn)
    
    welcome_text = (
        f"ሰላም {message.from_user.first_name}!\n\n"
        "እንኳን ወደ **SchoolBus ET** መተግበሪያ በደህና መጡ።\n"
        "ከታች ያለውን ቁልፍ በመጫን ሚኒ አፑን ይክፈቱ።"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

print("ቦቱ በስኬት መሥራት ጀምሯል...")
bot.polling()