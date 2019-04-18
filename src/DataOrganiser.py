class LeagueNames:
    BUNDESLIGA = "Bundesliga"
    EPL = "EPL"
    # SERIE_A = "Seria_A"
    # LA_LIGA = "La_Liga"
    # LIGUE_UN = "Ligue_Un"


class LeagueNamesUrls:
    EPL_URL = "premier-league/transfers/wettbewerb/GB1"
    BUNDESLIGA_URL_URL = "bundesliga/transfers/wettbewerb/L1"


class LeagueNameAndUrlMatcher:
    def __init__(self):
        self.league_name_url_map = {
            LeagueNames.BUNDESLIGA: LeagueNamesUrls.BUNDESLIGA_URL_URL,
            LeagueNames.EPL: LeagueNamesUrls.EPL_URL
        }


class League:
    def __init__(self, league_name):
        self.league_name = league_name
        self.transfers_for_year = {}