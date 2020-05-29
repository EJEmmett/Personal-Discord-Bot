import r6sapi


class Rank(r6sapi.Rank):
    _SEASONS = [
        "Operation Black Ice", "Operation Dust Line",
        "Operation Skull Rain", "Operation Red Crow",

        "Operation Velvet Shell", "Operation Health",
        "Operation Blood Orchid", "Operation White Noise",

        "Operation Chimera", "Operation Para Bellum",
        "Operation Grim Sky", "Operation Wind Bastion",

        "Operation Burnt Horizon", "Operation Phantom Sight",
        "Operation Ember Rise", "Operation Shifting Tides",

        "Operation Void Edge", "Operation Steel Wave"
    ]

    @property
    def season_name(self):
        return Rank._SEASONS[self.season - 1]


# Metaprogrammatically add unknown attrs
for attr in dir(Rank):
    if "__" not in attr and not hasattr(r6sapi.Rank, attr):
        setattr(r6sapi.Rank, attr, getattr(Rank, attr))
