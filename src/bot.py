from logging import Logger

import telegram
from injector import inject
from langfuse import get_client
from openinference.instrumentation.google_adk import GoogleADKInstrumentor
from telegram import Update, Message
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler

from agents.runner import reply_to_mention
from container import injector
from infrastructure.settings import Settings
from infrastructure.util import clean_markdown

applogger: Logger = injector.get(Logger)


async def send_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str, **kwargs) -> Message | None:
    """
    Sends a message, splitting it into multiple parts if it's too long.
    """
    max_length = telegram.constants.MessageLimit.MAX_TEXT_LENGTH
    text = clean_markdown(text)
    resulted_message = None
    for i in range(0, len(text), max_length):
        resulted_message = await context.bot.send_message(
            chat_id=chat_id,
            text=text[i:i + max_length],
            **kwargs
        )
    return resulted_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    user_language = user.language_code
    # applogger.info(f"User {user.first_name} started the bot. Language: {user_language}")

    if update.message.chat.type != "private":
        await update.message.delete()

    summary_formatted = (
        f"Hi! How can I assist you today, {user.first_name}?"
    )

    await send_message(
        context,
        chat_id=user_id,
        text=summary_formatted
    )


async def assistance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.text:
        return

    bot_message = await reply_to_mention(update.message.text, update, applogger)

    await send_message(
        context,
        chat_id=update.message.chat_id,
        text=bot_message,
        reply_to_message_id=update.message.message_id
    )


@inject
def main(settings: Settings, logger: Logger) -> None:
    logger.info("Initializing Langfuze client and tracing...")
    langfuse = get_client()
    # Verify connection
    if langfuse.auth_check():
        print("Langfuse client is authenticated and ready!")
    else:
        print("Authentication failed. Please check your credentials and host.")

    logger.info("Initializing Langfuze GoogleADKInstrumentor...")
    GoogleADKInstrumentor().instrument()

    print("Starting Telegram bot...")
    application = Application.builder().token(settings.get('telegram_bot_token')).build()

    # logger.info(settings.get('telegram_bot_token'))

    # Commands
    application.add_handler(CommandHandler("start", start))

    # Messages
    application.add_handler(MessageHandler(None, assistance))

    # applogger.info("Bot started. Listening for messages...")
    application.run_polling()


if __name__ == "__main__":
    injector.call_with_injection(main)
