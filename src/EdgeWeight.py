class EdgeWeight:
    def __init__(self, num_players=1, amount=0, total_adjusted_amount=0):
        self.num_players = num_players
        self.total_amount = amount
        self.total_adjusted_amount = total_adjusted_amount

    def increase_num_players(self):
        self.num_players += 1

    def increase_amount(self, new_amount):
        self.total_amount += new_amount

    def increase_adjusted_amount(self, new_adjusted_amount):
        self.total_adjusted_amount += new_adjusted_amount
