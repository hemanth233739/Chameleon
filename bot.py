import functools
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, InlineQueryHandler, Filters

from config import BOT_TOKEN
from constants import TRANSLATION_CHAT_ID
from handlers import group, game, dev, group_settings, private, stats

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename="log.log")


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True,
                      request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    dp = updater.dispatcher
    
    # Example of adding handlers with logging
    dp.add_handler(MessageHandler(Filters.group & (Filters.status_update.chat_created | Filters.status_update.new_chat_members), group.greeting))
    logging.info("Added greeting handler")

    # Add other handlers...
    dp.add_handler(CommandHandler("start", functools.partial(group.start, dp=dp), filters=Filters.group))
    
    # Error handling
    dp.add_error_handler(dev.error_handler)
    
    updater.start_polling(clean=True)
    updater.job_queue.run_repeating(stats.reload_sorted_players, 60*60*24, name="reload_sorted", first=0)
    updater.idle()


if __name__ == "__main__":
    main()
