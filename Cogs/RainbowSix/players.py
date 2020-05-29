import r6sapi

from .auth import Auth
from .ranks import Rank


class Player(r6sapi.Player):
    async def get_highest_rank(self) -> Rank:
        """

        Defaults to returning rank of NA servers
        """
        ranks = {}
        for region in Auth.valid_regions:
            rank = await self.get_rank(region)
            ranks[region] = rank

        ranks = sorted(ranks.items(), key=lambda tup: tup[1].rank_id, reverse=True)

        if ranks[0][1].rank_id == ranks[1][1].rank_id:
            ranks = sorted(ranks, key=lambda tup: tup[1].wins, reverse=True)

        if ranks[0][1].wins == ranks[1][1].wins or \
                ranks[1][1].wins == ranks[2][1].wins:
            for region, rank in ranks:
                if region == r6sapi.RankedRegions.NA:
                    return rank

        return ranks[0][1]


# Metaprogrammatically add unknown attrs
for attr in dir(Player):
    if "__" not in attr and not hasattr(r6sapi.Player, attr):
        setattr(r6sapi.Player, attr, getattr(Player, attr))
