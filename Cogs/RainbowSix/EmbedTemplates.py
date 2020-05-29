from datetime import datetime
from random import randint

from discord import Embed, Colour

from .auth import Auth


def _to_time(sec):
    day = sec // (24 * 3600)
    sec %= (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    return f"D: {day} H: {hour} M: {minutes}"


def general(player, rank):
    embed = Embed(title=f"*{rank.season_name}*",
                  colour=Colour(int(randint(0, 0xFFFFFF))),
                  timestamp=datetime.utcnow())

    embed.set_author(name=f"{Auth.get_region(rank.region)} - {player.name}",
                     url=player.url,
                     icon_url=player.icon_url)

    embed.set_thumbnail(url=rank.get_icon_url())
    embed.add_field(name="__Info__",
                    value=f"**Level**: {player.level} \
                                      \n**Rank**: {rank.rank} \
                                      \n**Time Played:**: {_to_time(player.time_played)}",
                    inline=True)
    embed.add_field(name="__Matches__",
                    value=f"**Total:** {player.matches_played}\
                                      \n**Wins:** {player.matches_won} \
                                      \n**Losses:** {player.matches_lost} \
                                      \n**W/L:** {(player.matches_won / (player.matches_won + player.matches_lost) * 100):.2f}%",
                    inline=True)
    embed.add_field(name="__Kills__",
                    value=f"**Kills:** {player.kills} \
                                      \n**Assists:** {player.kill_assists} \
                                      \n**Deaths:** {player.deaths} \
                                      \n**K/D/A:** {((player.kills + (3 / 4 * player.kill_assists)) / player.deaths):.2f}",
                    inline=True)
    return embed


def casual(player, rank):
    queue = player.casual

    embed = Embed(title=f"*{rank.season_name}*",
                  colour=Colour(int(randint(0, 0xFFFFFF))),
                  timestamp=datetime.utcnow())

    embed.set_thumbnail(url=rank.get_icon_url())
    embed.set_author(
        name=f"{Auth.get_region(rank.region)} {queue.name.title()} - {player.name}",
        url=player.url,
        icon_url=player.icon_url)

    embed.add_field(name="__Matches__",
                    value=f"**Wins:** {queue.won} \
                                \n**Losses:** {queue.lost} \
                                \n**W/L:** {queue.won / (queue.won + queue.lost) * 100:.2f}%",
                    inline=True)
    embed.add_field(name="__Kills__",
                    value=f"**Kills**: {queue.kills} \
                                 \n**Deaths**: {queue.deaths} \
                                 \n**K/D**: {queue.kills / queue.deaths:.2f}",
                    inline=True)

    return embed


def ranked(player, rank):
    queue = player.ranked

    embed = Embed(title=f"*{rank.season_name}*",
                  colour=Colour(int(randint(0, 0xFFFFFF))),
                  timestamp=datetime.utcnow())

    embed.set_author(
        name=f"{Auth.get_region(rank.region)} {queue.name.title()} - {player.name}",
        url=player.url,
        icon_url=player.icon_url)

    embed.set_thumbnail(url=rank.get_icon_url())
    embed.add_field(name="__Rank__",
                    value=f"**Current MMR**: {rank.mmr:.2f} \
                             \n**Current Rank**: {rank.rank} \
                             \n**Max MMR**: {rank.max_mmr:.2f} \
                             \n**Max Rank**: {rank.RANKS[rank.max_rank]}",
                    inline=True)
    embed.add_field(name="__Matches__",
                    value=f"**Wins:** {rank.wins} \
                             \n**Losses:** {rank.losses} \
                             \n**W/L:** {rank.wins / (rank.wins + rank.losses) * 100:.2f}%",
                    inline=True)
    embed.add_field(name="__Kills__",
                    value=f"**Kills**: {queue.kills} \
                                 \n**Deaths**: {queue.deaths} \
                                 \n**K/D**: {queue.kills / queue.deaths:.2f}",
                    inline=True)

    return embed
