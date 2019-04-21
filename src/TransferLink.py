class TransferLink:
    def __init__(self, source_team_id, target_team_id, amount=0, player_pos=None,
                 player_name=None, player_nationality=None,
                 source_team_league=None, target_team_league=None, source_team_name=None, target_team_name=None):
        self.source_team_id = source_team_id
        self.target_team_id = target_team_id
        self.amount = amount
        self.player_pos = player_pos
        self.player_name = player_name
        self.player_nationality = player_nationality
        self.source_team_league = source_team_league
        self.target_team_league = target_team_league
        self.source_team_name = source_team_name
        self.target_team_name = target_team_name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.source_team_id == other.source_team_id and self.target_team_id == other.target_team_id
        return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.source_team_id != other.source_team_id or self.target_team_id != other.target_team_id
        return False

    def __str__(self):
        return self.source_team_id + "," + self.target_team_id

    def __hash__(self):
        return hash(str(self))

    def show_info(self):
        print(self.player_name + ", " + self.player_pos + ", " + self.source_team_id + ", " + self.source_team_name + ", " +
              self.target_team_id + ", " + self.target_team_name + ", " + str(self.amount))


