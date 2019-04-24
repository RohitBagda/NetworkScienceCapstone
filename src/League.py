class League:
    def __init__(self, league_name):
        self.league_name = league_name
        self.transfers_for_year = {}
        self.clubs = set()
        self.all_transfers = []
        self.loan_tranfers = []

    def show_transfers_for(self, start_year, end_year):
        for year in range(start_year, end_year + 1):
            print("=======showing the links for " + str(year))
            try:
                for link in self.transfers_for_year[year]:
                    link.show_info()
            except Exception as e:
                print(e)

    def show_all_teams_belonging_to_league(self):
        print("=====================showing " + str(
            len(self.team_ids)) + " teams in" + self.league_name + "==================")
        for club in self.clubs:
            print(str(club.club_id) + "," + club.club_name)
        print("-----------done showing teams in " + self.league_name + "------------------")