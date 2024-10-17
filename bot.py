import functools
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, Filters

from config import BOT_TOKEN
from constants import TRANSLATION_CHAT_ID
from handlers import group, game, dev, group_settings, private, stats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)  # Log to console

def main():
    updater = Updater(token=BOT_TOKEN, request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    dp = updater.dispatcher

    # Adding handlers with logging
    dp.add_handler(MessageHandler(Filters.group & (Filters.status_update.chat_created | Filters.status_update.new_chat_members), group.greeting))
    logging.info("Added greeting handler")

    dp.add_handler(CommandHandler("start", functools.partial(group.start, dp=dp), filters=Filters.group))
    logging.info("Added start command handler")

    # Error handling
    dp.add_error_handler(dev.error_handler)

    # Start polling
    updater.start_polling(clean=True)
    logging.info("Bot started polling")
    
    # Scheduled job
    updater.job_queue.run_repeating(stats.reload_sorted_players, 60*60*24, name="reload_sorted", first=0)
    logging.info("Scheduled job for reloading sorted players")

    updater.idle()
    logging.info("Bot stopped")

if __name__ == "__main__":
    main()
