import logging

import discord
from discord.ext import commands
from discord.utils import get


class Guest(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("Bot." + __name__)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.add_roles(get(member.guild.roles, name="Guest"))
        self.logger.info(f"{member.display_name} has joined {member.guild}")


def setup(bot):
    bot.add_cog(Guest(bot))
