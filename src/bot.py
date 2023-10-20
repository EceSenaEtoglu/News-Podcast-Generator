from audio import *
from config import *
from api_wrapper import Api

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os

# GLOBALS
START_MESSAGE = "I can get you the top headlines and breaking news for a country (in the country's official language) in an audited format! \n" \
                "\nHere is what I can do:\n\n" \
                "1- Get news for a country from the country's sources.\n" \
                "2- Get news for a country from the country's sources about a specific category. Here are possible " \
                "categories:\n" \
                "   - business\n" \
                "   - entertainment\n" \
                "   - general\n" \
                "   - health\n" \
                "   - science\n" \
                "   - sports\n" \
                "   - technology\n\n" \
                "For option 1, type /getnews\n" \
                "For option 2, type /getnews_category\n"

INVALID_RESPONSE_ERROR = "I'm not sure I understand your response. To see what I can do type /start"

api = Api(NEWS_API_KEY)


# Commands
async def start_command(update: Update, context):
    """handle the /start command"""
    await update.message.reply_text(START_MESSAGE)


async def getnews(update: Update, context):
    """handle the /getnews command"""
    info_message = "To get top headlines and breaking news in an audited format:\n" \
                   "type (without '< >'):\n <insert a 2 letter country code in ISO 3166-1 (us,de,tr...)>'"

    await update.message.reply_text(info_message)


async def getnews_category(update: Update, context):
    """handle the /getnews_category command"""

    info_message = "Here are possible categories:\n" \
                   "   - business\n" \
                   "   - entertainment\n" \
                   "   - general\n" \
                   "   - health\n" \
                   "   - science\n" \
                   "   - sports\n" \
                   "   - technology\n\n" \
                   "To get top headlines and breaking news in an audited format:\n" \
                   "type (without '< >'):\n <insert a 2 letter country code in ISO 3166-1 (us,de,tr...)><insert space> " \
                   "<insert one of the categories above>"

    await update.message.reply_text(info_message)


# Logic
def get_audio(context, intro: str, operation: str, outputfile_name, country_code: str, category=None):
    """Create audio based on operation, return the audio path"""
    if operation == "getnews":
        articles = api.get_top_headlines(country_code)

        # create audio
        audio = Audio.from_country_code(articles, country_code, intro, outputfile_name)
        audio.create_audio()

        return audio.OUTPUT_NAME

    elif operation == "getnews_category":

        articles = api.get_top_headlines(country_code, category)

        # create audio
        audio = Audio.from_country_code(articles, country_code, intro, outputfile_name)
        audio.create_audio()

        return audio.OUTPUT_NAME


async def process_user_message(user_message: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Identify operation based on user_message

    If operation is not valid reply with a warning string

    Else reply with operation string, apply operation and return created path
    Return: path of the created audio"""

    # audio output file name if audio will be generated
    output_file_name = f"{update.message.chat_id}.mp3"

    response_data = user_message.split(" ")
    # user possibly asked for news in a country
    if len(response_data) == 1:

        # get list of articles
        country_code = response_data[0]

        # if given country code is valid
        if helpers.is_a_supported_country_code(country_code):

            audio_intro = f"latest news in {helpers.get_country_name(country_code)}"
            bot_response = f"Retrieving {audio_intro}. Loading..."
            await update.message.reply_text(bot_response)

            return get_audio(context, audio_intro, "getnews", output_file_name, country_code)

        # given country code is not valid
        else:

            bot_response = f"Country code '{country_code}' is not supported.\nPlease check if it is in 2 letter ISO 3166-1 format.If it is, please contact admin.\n" \
                           f"Did you want something else? Type /start to view my capabilities."

            await update.message.reply_text(bot_response)

    # user possibly asked for news in a country in a specific category

    elif len(response_data) == 2:

        # get list of articles
        country_code = response_data[0]
        category = response_data[1]

        # if given country code is valid
        if helpers.is_a_supported_country_code(country_code):

            if category in api.CATEGORIES:

                audio_intro = f"latest news in {helpers.get_country_name(country_code)} about {category}"
                bot_response = f"Retrieving {audio_intro}. Loading..."
                await update.message.reply_text(bot_response)

                return get_audio(context, audio_intro, "getnews_category", output_file_name, country_code, category)

            # category is not valid
            else:
                bot_response = f"Category '{category}' is not supported.\nTo see the supported categories type /getnews_category"
                await update.message.reply_text(bot_response)

        else:
            bot_response = f"Country code '{country_code}' is not supported.\nPlease check if it is in 2 letter ISO 3166-1 format." \
                           f"If it is, please contact admin.\nDid you want something else? Type /start to view my capabilities."
            await update.message.reply_text(bot_response)

    # unidentified response structure
    else:
        bot_response = INVALID_RESPONSE_ERROR
        await update.message.reply_text(bot_response)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user message

    Send audio to chat if audio was created else send error message """

    # identify if group or private
    message_type = update.message.chat.type

    # user response
    user_response = update.message.text

    if message_type == "group":

        if BOT_USERNAME in user_response:
            user_response = user_response.replace(BOT_USERNAME, "")
            audio_path = await process_user_message(user_response, update, context)

        else:
            return
    else:
        audio_path = await process_user_message(user_response, update, context)

    if audio_path:
        try:
            with open(audio_path, 'rb') as audio:
                await update.message.reply_audio(audio=audio)
        except FileNotFoundError as e:
            print(e)

        finally:
            # delete generated audio
            os.remove(audio_path)


# Debugger function for the developer
async def log_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


def main():
    print("Starting bot")
    app = Application.builder().token(TELEGRAM_BOT_API_KEY).build()

    # Handling Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler("getnews", getnews))
    app.add_handler(CommandHandler("getnews_category", getnews_category))

    # Handling Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(log_error)

    # Polls the bot
    print("Polling")
    # Check for updates every poll_interval
    app.run_polling(poll_interval=POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
