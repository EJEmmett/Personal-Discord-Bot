import r6sapi as api


class Auth(api.Auth):
    _REGIONS = {
        "na": api.RankedRegions.NA,
        "us": api.RankedRegions.NA,
        "america": api.RankedRegions.NA,
        "eu": api.RankedRegions.EU,
        "europe": api.RankedRegions.EU,
        "asia": api.RankedRegions.ASIA,
        "au": api.RankedRegions.ASIA,
        "anz": api.RankedRegions.ASIA,
        "oceania": api.RankedRegions.ASIA
    }

    __REGIONS = {
        api.RankedRegions.NA: "na",
        api.RankedRegions.EU: "eu",
        api.RankedRegions.ASIA: "asia"
    }

    _PLATFORMS = {
        "xb1": api.Platforms.XBOX,
        "xone": api.Platforms.XBOX,
        "xbone": api.Platforms.XBOX,
        "xbox": api.Platforms.XBOX,
        "xboxone": api.Platforms.XBOX,
        "ps": api.Platforms.PLAYSTATION,
        "ps4": api.Platforms.PLAYSTATION,
        "playstation": api.Platforms.PLAYSTATION,
        "uplay": api.Platforms.UPLAY,
        "pc": api.Platforms.UPLAY
    }

    __PLATFORMS = {
        api.Platforms.XBOX: "xb1",
        api.Platforms.PLAYSTATION: "ps4",
        api.Platforms.UPLAY: "uplay"
    }

    regions = list(_REGIONS.keys())
    platforms = list(_PLATFORMS.keys())
    valid_regions = set(_REGIONS.values())
    valid_platforms = set(_PLATFORMS.values())

    def __init__(self, *args, **kwargs):
        test_connection = kwargs.pop("test_connection", False)
        super().__init__(*args, **kwargs)

    def __del__(self):
        self.close()

    @staticmethod
    def get_platform(platform):
        if platform:
            if platform in Auth._PLATFORMS:
                return Auth._PLATFORMS.get(platform.lower())
            elif platform in Auth.valid_platforms:
                return Auth.__PLATFORMS.get(platform).upper()

        return api.Platforms.UPLAY

    @staticmethod
    def get_region(region):
        if region:
            if region in Auth._REGIONS:
                return Auth._REGIONS.get(region.lower())
            elif region in Auth.valid_regions:
                return Auth.__REGIONS.get(region).upper()

        return api.RankedRegions.NA

    @staticmethod
    def get_attrs(platform, region):
        return Auth.get_platform(platform), Auth.get_region(region)
