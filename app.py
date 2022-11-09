import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import pytz
import datetime

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi! Use /sub to subscribe to the bot")


async def notification(context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.datetime.now()
    datee = now.strftime("%Y-%m-%d")
    api_url = "https://clist.by/api/v2/contest/?username=sujalmaiti123456&api_key=45e98f4129e4ec36d065b5d91e5f184902d1fe2d&start__gt=" + datee + "T00%3A01&start__lt=" + datee + "T23%3A59"
    response = requests.get(api_url)
    res = dict(response.json())
    obj = res['objects']
    msg = "START-TIME LINK\n"
    for i in obj:
        start = str(i['start'])
        start = start[:10] + " " + start[11:]
        href = i['href']
        msg += start + " " + href + "\n"
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"{msg}")



async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    print(chat_id)
    context.job_queue.run_daily(notification, datetime.time(hour=23,minute=00,  tzinfo=pytz.timezone('Asia/Kolkata')), chat_id=chat_id, name=str(chat_id))
    text = "Subscribed" + str(chat_id)
    await update.effective_message.reply_text(text)


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5706620157:AAHH5Igx1OIp4WeCvp2-Lcr-T_gKBqOf05U").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("sub", sub))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()