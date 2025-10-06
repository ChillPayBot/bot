import asyncio
import logging
import sys

from dotenv import load_dotenv

from bot.main_bot import run_bot
from config.settings import get_settings, Settings

async def main():
    load_dotenv()
    settings = get_settings()

    await run_bot(settings)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped manually")
    except Exception as e_global:
        logging.critical(f"Global unhandled exception in main: {e_global}",
                         exc_info=True)
        sys.exit(1)