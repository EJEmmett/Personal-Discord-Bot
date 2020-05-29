from os import environ
from typing import Tuple

import r6sapi as api
from discord.ext import commands

from . import EmbedTemplates
from .auth import Auth
from .players import Player
from .ranks import Rank


class RainbowSix(commands.Cog):
    """ Utilizes RainbowSixSiege-Python-API by billyoyo to fetch user statistics """

    def __init__(self, bot: commands.Bot):
        self.unload_cog = False
        self.bot = bot

        try:
            self.auth = Auth(environ.get('USER'), environ.get('PASSWORD'),
                             max_connect_retries=3)  # , test_connection=True)
        except api.FailedToConnect as e:
            raise e

    @commands.group(
        name='r6s',
        aliases=['r6', 'stats'],
        description="Shows a users stats",
        help="""/r6s user - Show overall stats
                /r6s casual user - Show casual stats.
                /r6s rank user - Show ranked stats.
             """,
        invoke_without_command=True
    )
    async def r6s(self, ctx: commands.Context, username: str, platform: str = 'UPLAY'):
        """
        :param ctx - Discord Context
        :param username - Username
        :param platform - uplay, xbox, ps4
        """
        async with ctx.typing():
            platform = self.auth.get_platform(platform)

            try:
                player, rank = await self.get_player_data(username, platform)
            except api.InvalidRequest as e:
                if "No results" in e.args[0]:
                    await ctx.send("Player not found.")
                return

            embed = EmbedTemplates.general(player, rank)
            await ctx.send(embed=embed)

    @r6s.command(
        aliases=['c']
    )
    async def casual(self, ctx: commands.Context, username: str, platform: str = "uplay"):
        async with ctx.typing():
            platform = self.auth.get_platform(platform)

            try:
                player, rank = await self.get_player_data(username, platform)
            except api.InvalidRequest as e:
                if "No results" in e.args[0]:
                    await ctx.send("Player not found.")
                return

            embed = EmbedTemplates.casual(player, rank)
            await ctx.send(embed=embed)

    @r6s.command(
        aliases=['ranked', 'r']
    )
    async def rank(self, ctx: commands.Context, username: str, platform: str = "uplay",
                   region: str = "NA"):
        async with ctx.typing():
            platform, region = self.auth.get_attrs(
                *self._parameter_rearrange(platform, region)
            )

            try:
                player, rank = await self.get_player_data(username, platform)
            except api.InvalidRequest as e:
                if "No results" in e.args[0]:
                    await ctx.send("Player not found.")
                return

            embed = EmbedTemplates.ranked(player, rank)
            await ctx.send(embed=embed)

    async def get_player_data(self, username: str, platform: str, region=None):
        """|coro

        """
        player = await self.auth.get_player(name=username, platform=platform)

        if not region:
            rank = await player.get_highest_rank()
        else:
            rank = await player.get_rank(region)

        await player.check_queues()
        await player.check_general()
        await player.check_level()

        return player, rank

    @staticmethod
    def _parameter_rearrange(platform, region) -> Tuple[str, str]:
        """ Reduce complexity of entrance method """
        platform = platform.lower()
        region = region.lower()

        if platform in Auth.regions and region in Auth.platforms:
            platform, region = region, platform
        elif platform in Auth.regions:
            region = platform
        elif region in Auth.platforms:
            platform = region

        return platform, region


def setup(bot):
    bot.add_cog(RainbowSix(bot))
