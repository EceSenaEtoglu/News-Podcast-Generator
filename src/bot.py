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
def _handle_response(user_response:str,user_id:str) -> str:
    """handles user response, creates audio if applic. and returns the path"""

    response_data = user_response.split(" ")
    if len(response_data) == 1:
        country_code = response_data[0]

        return "hey there"

    return "what?"

async def _send_audio(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """"sends audio to chat"""

    # identify if group or private
    message_type = update.message.chat.type

    # user response
    user_response = update.message.text

    user_id = update.message.chat.id

    if message_type == "group":

        if BOT_USERNAME in user_response:
            parsed_response = user_response.replace(BOT_USERNAME,"")
            path = _handle_response(parsed_response,user_id)

        else:
            return
    else:
        path = _handle_response(user_response,user_id)

    await update.message.reply_audio(path)

async def error(update:Update, context:ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot")
    app = Application.builder().token(TELEGRAM_BOT_API_KEY).build()

    # Make sure you add the commands via telegram UI

    # Handling Commands
    app.add_handler(CommandHandler('start',_start_command))

    # Handling Messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling")
    # Check for updates every poll_interval
    app.run_polling(poll_interval=POLL_INTERVAL)
