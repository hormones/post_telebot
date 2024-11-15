# I am developing a Telegram post bot. Users can initiate a post by sending any text. The tech stack used is Python(3.12) + SQLite3 + python-telegram-bot(21.5) framework.

# The project structure is as follows:
# - `commands` folder: Contains the Python files for bot commands.
# - `base` folder: Contains the Python files for database operations, utility classes, etc.
# - `config.py`: Configuration file.
# - `main.py`: Main executable program.
# - Other folders and files: Not important, please ignore them.

import asyncio
import logging


import config, db, commands, buttons, post
from config import APP


# Main async function to run the bot
async def main():
    await db.init()
    await config.init()
    await commands.init()
    await buttons.init()
    await post.init()

    # Initialize the bot
    await APP.initialize()

    # Start the bot using run_polling
    await APP.updater.start_polling()

    # Start the bot
    await APP.start()

    try:
        # This will keep it running until Ctrl+C
        await asyncio.Event().wait()
    finally:
        await APP.updater.stop()
        await APP.stop()
        await APP.shutdown()
        await db.close()


# Entry point of the script
if __name__ == "__main__":
    try:
        # Run the asyncio event loop
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
