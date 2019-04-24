class EdgeWeight:
    def __init__(self, num_players=1, amount=0):
        self.num_players = num_players
        self.total_amount = amount

    def increase_num_players(self):
        self.num_players += 1

    def increase_amount(self, new_amount):
        self.total_amount += new_amount
