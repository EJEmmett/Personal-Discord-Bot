import logging
from os import environ

from discord.ext import commands
from dotenv import load_dotenv

import config
from Utils.Logging import setup_logging


def init(bot):
    logger = logging.getLogger("Bot")
    logger.info('Starting Bot...')

    @bot.event
    async def on_ready():
        logger.info(f"Logged in as {bot.user.name} - {bot.user.id}")

        for cog in config.cogs:
            bot.load_extension(cog)

def main():
    load_dotenv()
    setup_logging()
    bot = commands.Bot(
        command_prefix=config.prefix,
        description=config.description,
        owner=config.owner
    )
    init(bot)
    bot.run(environ.get('BOT_TOKEN'), reconnect=True)


if __name__ == '__main__':
    main()
