import os
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Define a function to handle incoming messages
def download_and_upload(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    text = update.message.text

    # Check if the message is a valid URL
    if text.startswith("http"):
        try:
            # Download the content from the provided link
            response = requests.get(text)
            if response.status_code == 200:
                file_extension = os.path.splitext(text)[1]
                # Save the downloaded content as a temporary file
                with open(f"temp{file_extension}", "wb") as file:
                    file.write(response.content)

                # Upload the downloaded file to the Telegram chat
                context.bot.send_document(chat_id=chat_id, document=open(f"temp{file_extension}", "rb"))

                # Clean up the temporary file
                os.remove(f"temp{file_extension}")
            else:
                context.bot.send_message(chat_id=chat_id, text="Failed to download the file.")
        except Exception as e:
            context.bot.send_message(chat_id=chat_id, text=f"Error: {str(e)}")
    else:
        context.bot.send_message(chat_id=chat_id, text="Please provide a valid download link.")

# Create an Updater and pass in your bot's API token
updater = Updater(token='xxxx', use_context=True)

# Get the dispatcher to register handlers
dp = updater.dispatcher

# Register a message handler for your bot
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_and_upload))

# Start the bot
updater.start_polling()
updater.idle()
