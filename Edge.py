class Edge:
    def __init__(self, source_team, target_team, amount=0, player_pos=None,
                 player_name=None, player_nationality=None,
                 source_team_league=None, target_team_league=None):
        self.source_team = source_team
        self.target_team = target_team
        self.amount = amount
        self.player_pos = player_pos
        self.player_name = player_name
        self.player_nationality = player_nationality
        self.source_team_league = source_team_league
        self.target_team_league = target_team_league

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.source_team == other.source_team and self.target_team == other.target_team
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.source_team != other.source_team or self.target_team != other.target_team
        return False

    def __str__(self):
        return self.source_team + "," + self.target_team

    def __hash__(self):
        return hash(str(self))



