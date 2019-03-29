from random import randint  # Randomly generate a color for the embed
from typing import Optional  # Provides type specification and optional parameters

from discord import Embed, Colour, Member  # Embed creation and color specification
from discord.ext import commands  # Discord Rewrite branch, Cogs and Command addition
from tinydb import TinyDB, Query  # Json based database service

import secrets  # Secrets


class EpicPoints(commands.Cog):
    """
    Rewards discord members based on how often they use epic words
    Punishes them for saying un-epic words
    """
    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('data.json').table('users')
        self.users = Query()

    @commands.Cog.listener()
    async def on_ready(self):
        for u in self.bot.get_all_members():
            if not (self.db.contains(u.id == self.users.id) or u.bot):
                self.db.insert({'id': u.id, 'points': "100"})

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not self.db.contains(member.id == self.users.id):
            self.db.insert({'id': member.id, 'points': "100"})

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.author.id == self.bot.user.id and \
                                        self.db.contains(message.author.id == self.users.id):

            cur = self.db.get(self.users['id'] == message.author.id)

            epic_count_points = sum(map(message.content.lower().count,
                                        secrets.epic_words))*secrets.epic_weight
            unepic_count_points = sum(map(message.content.lower().count,
                                          secrets.unepic_words))*secrets.unepic_weight

            points = int(cur['points']) + epic_count_points - unepic_count_points
            print("Create:", message.author.display_name+": ("+str(cur['points'])+")",
                  "+"+str(epic_count_points), "-"+str(unepic_count_points))
            self.db.update({'points': str(points)}, self.users.id == message.author.id)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot and not message.author.id == self.bot.user.id and \
                                          self.db.contains(message.author.id == self.users.id):

            cur = self.db.get(self.users['id'] == message.author.id)

            epic_count_points = sum(map(message.content.lower().count,
                                        secrets.epic_words))*secrets.epic_weight
            unepic_count_points = sum(map(message.content.lower().count,
                                          secrets.unepic_words))*secrets.unepic_weight

            points = int(cur['points']) - epic_count_points + unepic_count_points
            print("Delete:", message.author.display_name+": ("+str(cur['points'])+")",
                  "+"+str(unepic_count_points), "-"+str(epic_count_points))
            self.db.update({'points': str(points)}, self.users.id == message.author.id)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot and not after.author.id == self.bot.user.id and \
               self.db.contains(after.author.id == self.users.id):

            cur = self.db.get(self.users['id'] == after.author.id)

            b_epic_count_points = sum(map(before.content.lower().count,
                                          secrets.epic_words))*secrets.epic_weight
            b_unepic_count_points = sum(map(before.content.lower().count,
                                            secrets.unepic_words))*secrets.unepic_weight

            a_epic_count_points = sum(map(after.content.lower().count,
                                          secrets.epic_words))*secrets.epic_weight
            a_unepic_count_points = sum(map(after.content.lower().count,
                                            secrets.unepic_words))*secrets.unepic_weight

            b_points = b_epic_count_points - b_unepic_count_points
            a_points = a_epic_count_points - a_unepic_count_points
            o_points = b_points - a_points
            points = int(cur['points']) - o_points
            print("Edit:", after.author.display_name+": ("+str(cur['points'])+")",
                  str(a_points), str(b_points))

            self.db.update({'points': str(points)}, self.users.id == after.author.id)

    @commands.command(
        name='points',
        description="""Shows a users point value
           /points - Shows your own points
           /points [member] - Shows a members points
            """,
        aliases=['p']
    )
    async def points(self, ctx, member: Optional[Member]):
        if member:
            cur = self.db.get(self.users['id'] == member.id)
            embed = Embed(title="Epic Points", colour=member.top_role.colour)
            if len(cur['points']) <= 1024:
                embed.add_field(name=member.display_name, value=format(int(cur['points']), ','), inline=False)
            else:
                await ctx.send("{0} has {1} points".format(member.display_name, format(int(cur['points']), ',')))
                return

        else:
            cur = self.db.get(self.users['id'] == ctx.author.id)
            embed = Embed(title="Epic Points", colour=ctx.author.top_role.colour)
            if len(cur['points']) <= 1024:
                embed.add_field(name=ctx.author.display_name, value=format(int(cur['points']), ','), inline=False)
            else:
                await ctx.send("You have {0} points".format(format(int(cur['points']), ',')))
                return

        await ctx.send(embed=embed)
        return

    @commands.command(
        name='leaderboard',
        description='Shows a leaderboard of the top 10 users',
        aliases=['lb']
    )
    async def leaderboard(self, ctx):
        """ Shows a leaderboard of the top 10 users """
        full = sorted(self.db.all(), key=lambda x: int(x['points']), reverse=True)
        embed = Embed(title="Leaderboard", description="Okay, This Is Epic.", colour=Colour(int(randint(0, 0xFFFFFF))))
        for p, l in enumerate(full[0:10]):
            u = await self.bot.fetch_user(l['id'])
            name = "#{0} {1}".format(p+1, u.display_name)
            embed.add_field(name=name, value="{0} points".format(int(l['points']), ','), inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        hidden=True,
        name='set',
        description='Sets a users points',
        aliases=['s']
    )
    @commands.is_owner()
    async def set_points(self, ctx, member: Optional[Member], give_points):
        """ Set user points """
        if member:
            self.db.update({'points': give_points}, self.users.id == member.id)
            await ctx.send("Set {0} to {1} Epic points.".format(member.nick, give_points))
        else:
            self.db.update({'points': give_points}, self.users.id == ctx.author.id)
            await ctx.send("Set you to {0} Epic points.".format(give_points))

    @commands.command(
        hidden=True,
        name='give',
        description='Gives a users points',
        aliases=['g']
    )
    @commands.is_owner()
    async def give(self, ctx, member: Optional[Member], give_points: int):
        """ Give user points """
        if member:
            cur = self.db.get(self.users['id'] == member.id)
            points = int(cur['points']) + give_points
            self.db.update({'points': str(points)}, self.users.id == member.id)
            await ctx.send("Gave {0} {1} Epic points.".format(member.nick, give_points))
        else:
            cur = self.db.get(self.users['id'] == ctx.author.id)
            points = int(cur['points']) + give_points
            self.db.update({'points': str(points)}, self.users.id == ctx.author.id)
            await ctx.send("Gave you {0} Epic points.".format(give_points))


def setup(bot):
    b = EpicPoints(bot)
    bot.add_cog(b)
