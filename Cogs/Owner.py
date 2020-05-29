import logging
from typing import Optional

from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("Bot." + __name__)

    @staticmethod
    def _min(num: int, ctx):
        return

    @commands.command(name='age', hidden=True)
    @commands.is_owner()
    async def age(self, ctx: commands.Context, num: Optional[int] = 5):
        string = f"Oldest {num} Users\n"
        for pos, member in enumerate(
                sorted(list(ctx.guild.members), key=lambda k: k.joined_at)[0:num]):
            string += f"{pos + 1}. {member.display_name} - {member.joined_at}\n"

        await ctx.send(string)

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        cog = "Cogs." + cog
        try:
            self.bot.load_extension(cog)
            self.logger.info("Loaded Cog: %s", cog)
        except Exception as e:
            self.logger.exception(e)

        await ctx.message.delete()

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def unload(self, ctx: commands.context, *, cog: str):
        cog = "Cogs." + cog
        try:
            self.bot.unload_extension(cog)
            self.logger.info("Unloaded Cog: %s", cog)
        except Exception as e:
            self.logger.exception(e)

        await ctx.message.delete()

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx: commands.context, *, cog: str):
        cog = "Cogs." + cog
        try:
            self.bot.reload_extension(cog)
            self.logger.info("Reloaded Cog: %s", cog)
        except Exception as e:
            self.logger.exception(e)

        await ctx.message.delete()

    @commands.command(name='ping', hidden=True)
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency, 1)}ms')


def setup(bot):
    bot.add_cog(Owner(bot))
