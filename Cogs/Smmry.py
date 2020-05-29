import logging
from os import environ
from random import randint
from urllib.request import urlopen, Request

import favicon
from Smmry import SmmryAPI
from bs4 import BeautifulSoup
from discord import Embed, Colour
from discord.ext import commands
from tinydb import TinyDB, where
from tldextract import tldextract
from validators import url


class Smmry(commands.Cog):
    """ Utilizes smmryAPI from dsynkov at https://github.com/dsynkov/smmryAPI """

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                             'AppleWebKit/537.11 (KHTML, like Gecko) '
                             'Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

    images = {
        'left': "rGRc2cZ",
        'left center': "lyKaRCa",
        'center': "KvaqlAT",
        'right center': "pZU66MD",
        'right': "NJ6fDi5",
        'pro science': "uWM6CWd",
        'conspiracy': "4Ay1FYw",
        'fake news': "xRmAzyt",
        'satire': "IkKGfEv"
    }

    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('Databases/Bias.json').table('Sources')
        self.smmry = SmmryAPI(environ.get('SMMRY_KEY'))
        self.logger = logging.getLogger("Bot." + __name__)

    @commands.command(
        name='smmry',
        description="Summarize articles.",
        help="""/smmry url
             """,
    )
    async def smmry(self, ctx: commands.Context, *, article: str):
        """
        :param ctx: Discord Context, gives author name, id, channel sent in and others
        :param article: Link to article
        """

        async with ctx.typing():
            if not url(article):
                await ctx.send("Invalid URL")
                return

            self.logger.info(f"{ctx.author.display_name} has requested a summary of {article}")

            summary = self.smmry.summarize(article, sm_length=5)
            await self.generate_embed(ctx, article, summary)
            await ctx.message.delete()

    async def generate_embed(self, ctx, article, summary):
        source = self.db.get(where('Site').test(Smmry.domain_check, summary.sm_url))

        with urlopen(Request(url=article, headers=Smmry.headers)) as page:
            soup = BeautifulSoup(page, features="lxml")

        icon_link = favicon.get(article)[0].url

        color = soup.find("meta", property="theme-color")
        embed = Embed(title=f"*{soup.find('title').text}*",
                      url=summary.sm_url,
                      description=f"{summary.sm_api_content}",
                      colour=Colour(color['content']) if color
                      else Colour(int(randint(0, 0xFFFFFF))))

        embed.set_author(name=f"{source['Title'] if source else summary.sm_domain} ",
                         url=f"http://www.{summary.sm_domain}",
                         icon_url=icon_link)

        if source:
            leaning = " ".join(source['Leaning'].split("-"))
            bias_source = source['Link']
            img = f"https://i.imgur.com/{Smmry.images.get(leaning)}.png"

            if leaning == "satire":
                embed.set_footer(text=f"{leaning.title()} | {bias_source}",
                                 icon_url=img)
            elif leaning == "fake-news":
                embed.set_footer(
                    text=f"{leaning.title()} | Reasoning: {source['Factual']} | {bias_source}",
                    icon_url=img)
            else:
                embed.set_footer(
                    text=f"{leaning.title()} | Factuality: {source['Factual']} | {bias_source}",
                    icon_url=img)

        embed.add_field(name="__Requests remaining__",
                        value=f" {summary.sm_requests_remaining}/100",
                        inline=True)

        embed.add_field(name="__Requested By__",
                        value=f"{ctx.message.author.name}",
                        inline=True)
        embed.add_field(name="__Reduced By__",
                        value=f"{summary.sm_api_content_reduced}",
                        inline=True)

        await ctx.send(embed=embed)

    @staticmethod
    def domain_check(db_val, ext_val):
        return tldextract.extract(ext_val).registered_domain in db_val

    @smmry.error
    async def smmry_error(self, ctx, error):
        await ctx.send("Could not process request.")


def setup(bot):
    bot.add_cog(Smmry(bot))
