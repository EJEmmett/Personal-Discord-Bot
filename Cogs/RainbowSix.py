import asyncio  # Coroutine decorator and even loop initialization as well as return from async coroutine function
from datetime import datetime  # Add timestamp for embed
from random import randint  # Randomly generate a color for the embed
from typing import Optional  # Provides type specification and optional parameters

import nest_asyncio  # Enables Nested Event Loop
import r6sapi as api  # Rainbow Six API
from discord import Embed, Colour  # Embed creation and color specification
from discord.ext import commands  # Discord Rewrite branch, Cogs and Command addition

import secrets  # Secrets, not included in github


def _run(f):
    return asyncio.get_event_loop().run_until_complete(asyncio.gather(f))[0]


def _to_time(sec):
    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    return "D: {} H: {} M: {}".format(day, hour, minutes)


class RainbowSix(commands.Cog):
    """ Utilizes RainbowSixSiege-Python-API by billyoyo to fetch user statistics """
    _flag = True

    def __init__(self, bot):
        nest_asyncio.apply()
        try:
            self.auth = api.Auth(secrets.user, secrets.password, max_connect_retries=2)
        except api.FailedToConnect:
            RainbowSix._flag = False

        self.region_dict = {api.RankedRegions.NA: "NA", api.RankedRegions.EU: "EU",
                            api.RankedRegions.ASIA: "ASIA"}

        # Converts Human Readable string to Ubisoft region specifier string
        # 'None' specifies a default region
        self.human_dict = {"NA": api.RankedRegions.NA, "EU": api.RankedRegions.EU,
                           "ASIA": api.RankedRegions.ASIA, None: api.RankedRegions.NA}

        # 'None' specifies a default platform
        self.platform_dict = {"uplay": api.Platforms.UPLAY, "xbox": api.Platforms.XBOX,
                              "ps4": api.Platforms.PLAYSTATION, None: api.Platforms.UPLAY}

        self.season_list = ["Operation Black Ice", "Operation Dust Line", "Operation Skull Rain",
                            "Operation Red Crow", "Operation Velvet Shell", "Operation Health",
                            "Operation Blood Orchid", "Operation White Noise", "Operation Chimera",
                            "Operation Para Bellum", "Operation Grim Sky", "Operation Wind Bastion",
                            "Operation Burnt Horizon"]
        self.bot = bot

    @commands.command(
        name='stats',
        description="Shows a users stats",
        help="""/stats user - Show overall stats
                /stats user casual - Show casual stats.
                /stats user ranked - Show ranked stats.
                Optional:
                /stats user queue platform region - Shows user stats from queue on platform in region
             """,
        enabled=_flag
    )
    async def stats_super(self, ctx, player: str, queue: Optional[str], platform: Optional[str],
                          region: Optional[str]):
        """
        Entrance command
        Optional specifies that if nothing is given it defaults to None
        :param ctx - Discord Context, gives author name, id, channel sent in and others
        :param player - String specifying a username of an ubisoft account
        :param queue - Optional string arg, takes a queue (ranked, casual)
        :param platform - Optional string arg, takes a platform (uplay, xbox, ps4, None)
        :param region - Optional string arg, takes a region (NA, EU, ASIA, None)
        """
        async with ctx.channel.typing():
            if queue:
                queue = queue.casefold()

            # Enables the user to enter the platform or region in any order
            platform, region = self._parameter_rearrange(platform, region)

            if queue == "ranked":
                await self.stats_ranked_sub(ctx, player, platform, region)
            elif queue == "casual":
                await self.stats_casual_sub(ctx, player, platform, region)
            else:
                await self.stats_sub(ctx, player, platform)

    async def stats_ranked_sub(self, ctx, player, platform, region):

        (player, rank) = _run(self.get_user(player, platform, region))
        embed = Embed(title="*{}*".format(self.season_list[rank.season - 1]),
                      colour=Colour(int(randint(0, 0xFFFFFF))),
                      timestamp=datetime.utcnow())

        embed.set_author(name="{} Ranked - {}".format(self.region_dict[rank.region], player.name),
                         url=player.url,
                         icon_url=player.icon_url)

        embed.set_thumbnail(url=rank.get_icon_url())
        embed.add_field(name="__Rank__",
                        value="**Current MMR**: {:.2f} \
                             \n**Current Rank**: {} \
                             \n**Max MMR**: {:.2f} \
                             \n**Max Rank**: {}".format(rank.mmr, rank.rank, rank.max_mmr, rank.RANKS[rank.max_rank]),
                        inline=True)
        embed.add_field(name="__Matches__",
                        value="**Wins:** {} \
                             \n**Losses:** {} \
                             \n**W/L:** {:.2f}%".format(rank.wins, rank.losses, rank.wins/(rank.wins+rank.losses)*100),
                        inline=True)

        await ctx.send(embed=embed)

    async def stats_casual_sub(self, ctx, player, platform, region):

        player, rank, queue = _run(self.get_casual_user(player, platform, region))
        embed = Embed(title="*{}*".format(self.season_list[rank.season - 1]),
                      colour=Colour(int(randint(0, 0xFFFFFF))),
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=rank.get_icon_url())
        embed.set_author(name="{} Casual - {}".format(self.region_dict[rank.region], player.name),
                         url=player.url,
                         icon_url=player.icon_url)

        embed.add_field(name="__Matches__",
                        value="**Wins:** {} \
                            \n**Losses:** {} \
                            \n**W/L:** {:.2f}%".format(queue.won, queue.lost,
                                                       queue.won / (queue.won + queue.lost) * 100),
                        inline=True)
        embed.add_field(name="__Kills__",
                        value="**Kills**: {} \
                             \n**Deaths**: {} \
                             \n**K/D**: {:.2f}".format(queue.kills, queue.deaths, queue.kills/queue.deaths),
                        inline=True)

        await ctx.send(embed=embed)

    async def stats_sub(self, ctx, player, platform):

        player, rank = _run(self.get_user(player, platform, None))

        embed = Embed(title="*{}*".format(self.season_list[rank.season - 1]),
                      colour=Colour(int(randint(0, 0xFFFFFF))),
                      timestamp=datetime.utcnow())

        embed.set_author(name="{} - {}".format(self.region_dict[rank.region], player.name),
                         url=player.url,
                         icon_url=player.icon_url)

        embed.set_thumbnail(url=rank.get_icon_url())
        embed.add_field(name="__Info__",
                        value="**Level**: {} \
                              \n**Rank**: {} \
                              \n**Time Played:**: {}".format(player.level, rank.rank, _to_time(player.time_played)),
                        inline=True)
        embed.add_field(name="__Matches__",
                        value="**Total:** {}\
                              \n**Wins:** {} \
                              \n**Losses:** {} \
                              \n**W/L:** {:.2f}%".format(player.matches_played, player.matches_won, player.matches_lost,
                                                         (player.matches_won / (player.matches_won +
                                                                                player.matches_lost) * 100)),
                        inline=True)
        embed.add_field(name="__Kills__",
                        value="**Kills:** {} \
                              \n**Assists:** {} \
                              \n**Deaths:** {} \
                              \n**K/D/A:** {:.2f}".format(player.kills, player.kill_assists, player.deaths,
                                                          ((player.kills + (3 / 4 * player.kill_assists)) /
                                                           player.deaths)
                                                          ),
                        inline=True)

        await ctx.send(embed=embed)

    @asyncio.coroutine
    def get_user(self, player, platform, region):
        """ Used by stats_sub and stats_ranked_sub """
        player = yield from self.auth.get_player(player, self.platform_dict[platform.casefold() if platform else None])
        rank = yield from player.get_rank(self.human_dict[region.upper() if region else None])
        yield from player.check_queues()
        yield from player.check_level()
        yield from player.check_general()
        return player, rank

    @asyncio.coroutine
    def get_casual_user(self, player, platform, region):
        """ Used by stats_casual_sub """
        player = yield from self.auth.get_player(player, self.platform_dict[platform.casefold() if platform else None])
        rank = yield from player.get_rank(self.human_dict[region.upper() if region else None])
        yield from player.check_queues()
        return player, rank, player.casual

    def _parameter_rearrange(self, platform, region):
        """ Reduce complexity of entrance method """
        if not platform or not region:
            if platform and platform not in self.platform_dict:
                swap = platform
                region = platform
                platform = swap
            elif region and region not in self.human_dict:
                swap = region
                platform = region
                region = swap

        return platform, region

    @stats_super.error
    async def stats_super_handler(self, ctx, error):
        if isinstance(error, api.InvalidRequest):
            await ctx.send("I could not find that user.")

    @commands.command(
        name='test',
        hidden=True,
        enabled=_flag
    )
    async def test(self, ctx):
        await self.stats_sub(ctx, "Ed_emms", "uplay")


def setup(bot):
    bot.add_cog(RainbowSix(bot))
