from discord.ext import commands

import config
import secrets


def main(bot):
    print('Starting Bot...')

    @bot.event
    async def on_ready():
        print("Logged in as {} - {}".format(bot.user.name, bot.user.id))
        for cog in config.cogs:
            bot.load_extension(cog)


if __name__ == '__main__':
    bot = commands.Bot(
        command_prefix=config.prefix,
        description=config.description,
        owner=config.owner
        )
    main(bot)
    bot.run(secrets.bot_token, reconnect=True)
