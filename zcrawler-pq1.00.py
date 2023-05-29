from bs4 import BeautifulSoup
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Telegram bot token obtained from the BotFather
TOKEN = '5806601543:AAH2nVRQZBtgSYmXIsbPceKebwmJHKmUmvQ'

# Initialize the Telegram bot
bot = telegram.Bot(token=TOKEN)

# Handler for the /start command
def start(update, context):
    chat_id = update.effective_chat.id
    instructions = "Welcome to the PDF Scraping Bot!\n\n"
    instructions += "To retrieve PDF files, simply send the course code without any spaces.\n"
    instructions += "For example: UGRC150"
    context.bot.send_message(chat_id=chat_id, text=instructions)

# Handler for incoming messages
def handle_message(update, context):
    chat_id = update.effective_chat.id
    course_code = update.message.text.strip().upper()

    # Perform web scraping
    with open('index.html', 'r') as text_file:
        soup = BeautifulSoup(text_file, 'lxml')
        reference = soup.find_all('a', class_=course_code)

        if not reference:
            context.bot.send_message(chat_id=chat_id, text="No PDF files found for the given course code.")
            return

        for ref in reference:
            pdf_link = ref['href']
            send_pdf(chat_id, pdf_link)

# Function to send the PDF file to the user
def send_pdf(chat_id, pdf_link):
    try:
        response = requests.get(pdf_link)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        bot.send_message(chat_id=chat_id, text="An error occurred while accessing the PDF file.")
        return

    # Send the PDF file
    bot.send_document(chat_id=chat_id, document=response.content)

# Set up the Telegram bot
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
updater.start_polling()