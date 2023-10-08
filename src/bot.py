from api import *
from audio import *
from config import*
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

START_MESSAGE = "I can get you the top headlines and breaking news for a country in an audited format. In the specified country's language.\n" \
                "Here is what I can do:\n" \
                "1- Get news for a country from the country's sources.\n" \
                "2- Get news for a country from the country's sources about a specific category. Here are possible categories:\n" \
                "   - business\n" \
                "   - entertainment\n" \
                "   - general\n" \
                "   - health\n" \
                "   - science\n" \
                "   - sports\n" \
                "   - technology\n\n" \
                "For option 1, type /getnews_country'get \n."\
                "For option 2, type /getnews_countrycategory \n."

INVALID_RESPONSE_ERROR = "I'm not sure I understand your response. Let me show you what I can do"


api = Api(NEWS_API_KEY)

# Commands
async def _start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(START_MESSAGE)

async def _getnews_country_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    info_message = "To get top headlines and breaking news in an audited format:\n" \
                   "type this without '< >': <insert your country code according to ISO 3166-1>'"

    await update.message.reply_text(info_message)


async def _getnews_country_category_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    info_message = "Here are possible categories:\n" \
                "   - business\n" \
                "   - entertainment\n" \
                "   - general\n" \
                "   - health\n" \
                "   - science\n" \
                "   - sports\n" \
                "   - technology\n\n" \
        "To get top headlines and breaking news in an audited format:\n" \
        "type this without '< >': <insert your country code according to ISO 3166-1>'<insert space> <insert one of the categories above>"

    await update.message.reply_text(info_message)

async def _help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    start_message = "command that you get after \help"
    await update.message.reply_text(start_message)

# Logic

def _process_response(user_response:str, user_id) -> str:
    """Handles user response, creates audio if applicable and returns the abs path.
    If not applicable returns invalid response message"""

    response_data = user_response.split(" ")
    bot_response = INVALID_RESPONSE_ERROR
    output_file_name = f"{user_id}.mp3"

    # user possibly asked for news in a country
    if len(response_data) == 1:

        # get list of articles
        country_code = response_data[0]
        try:
            articles = api.get_top_headlines(country_code)

        # if country code is invalid
        except InvalidInputError:
            pass

        else:
            # intro to start the audio with
            intro = f"Latest news in {api.COUNTRIES.get(country_code)}"
            audio = Audio.from_country_code(articles,country_code,intro,output_file_name)

            # create audio
            if audio:
                audio.create_audio()
                bot_response = audio.get_audio_path()

            else:


    # user possibly asked for news in a country in a specific category
    elif len(response_data) == 2:

        # get list of articles
        country_code = response_data[0]
        category = response_data[1]
        try:
            articles = api.get_top_headlines(country_code,category)

        # if country code or category is invalid
        except InvalidInputError:
            pass

        else:

            # intro to start the audio with
            intro = f"Latest news in {api.COUNTRIES.get(country_code)} about {category}"
            audio = Audio.from_country_code(articles, country_code, intro, output_file_name)
            # create audio
            if audio:
                audio.create_audio()
                bot_response = audio.get_audio_path()
            else:

    return bot_response

async def _send_audio(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """"Sends audio to chat if audio was created else sends START_MESSAGE"""

    # identify if group or private
    message_type = update.message.chat.type

    # user response
    user_response = update.message.text

    user_id = update.message.chat.id

    if message_type == "group":

        if BOT_USERNAME in user_response:
            parsed_response = user_response.replace(BOT_USERNAME,"")
            system_response = _process_response(parsed_response, user_id)

        else:
            return
    else:
        system_response = _process_response(user_response, user_id)

    # if provided response is not valid
    # show start message
    if system_response == INVALID_RESPONSE_ERROR:
        await update.message.reply_text(INVALID_RESPONSE_ERROR)
        await update.message.reply_text(START_MESSAGE)

    elif system_response ==

    else:
        # send audio
        await update.message.reply_audio(system_response)


# Debugger function for the developer
async def log_error(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot")
    app = Application.builder().token(TELEGRAM_BOT_API_KEY).build()


    # Handling Commands
    app.add_handler(CommandHandler('start',_start_command))

    # Handling Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    # Errors
    app.add_error_handler(log_error)

    # Polls the bot
    print("Polling")
    # Check for updates every poll_interval
    app.run_polling(poll_interval=POLL_INTERVAL)from config import*


