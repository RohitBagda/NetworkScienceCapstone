class EdgeWeight:
    def __init__(self, num_players=1, amount=0, total_adjusted_amount=0, num_young_players=0,
                 num_middle_aged_players=0, num_old_players=0):
        self.num_players = num_players
        self.total_amount = amount
        self.total_adjusted_amount = total_adjusted_amount
        self.num_young_players = num_young_players
        self.num_middle_aged_players = num_middle_aged_players
        self.num_old_players = num_old_players

    def increase_num_players(self):
        self.num_players += 1

    def increase_amount(self, new_amount):
        self.total_amount += new_amount

    def increase_adjusted_amount(self, new_adjusted_amount):
        self.total_adjusted_amount += new_adjusted_amount

    def increase_num_young_players(self):
        self.num_young_players += 1

    def increase_num_old_players(self):
        self.num_old_players += 1

    def increase_num_middle_aged_players(self):
        self.num_middle_aged_players += 1
