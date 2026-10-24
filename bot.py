import os
import threading
import telebot
from telebot import types
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Render ፖርት እንዲያይ የሚያደርግ ትንሽ ዌብ ሰርቨር
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SchoolBus ET Bot & Mini App is running 24/7!")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# ሰርቨሩን ከቦቱ ጋር በትይዩ (Background Thread) ማስጀመር
server_thread = threading.Thread(target=run_http_server, daemon=True)
server_thread.start()

# 2. የቴሌግራም ቦት ማዋቀሪያ
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise ValueError("TELEGRAM TOKEN is not set in environment variables!")

bot = telebot.TeleBot(TOKEN)

WEB_APP_URL = 'https://splendorous-mermaid-b768fa.netlify.app'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    web_app_btn = types.InlineKeyboardButton(
        text="🚌 SchoolBus ET ሚኒ አፕ",
        web_app=types.WebAppInfo(url=WEB_APP_URL)
    )
    
    markup.add(web_app_btn)
    
    welcome_text = (
        f"ሰላም {message.from_user.first_name}!\n\n"
        "እንኳን ወደ **SchoolBus ET** መተግበሪያ በደህና መጡ።\n"
        "ከዚህ በታች ያለውን ቁልፍ በመጫን ሚኒ አፑን ይክፈቱ።"
    )
    
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode="Markdown")

# ቦቱን ማስጀመር
if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling()
