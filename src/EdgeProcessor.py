class EdgeProcessor:

    def __init__(self):
        pass

    def show_edges_with_amounts_as_weights(self, list_edges):
        edges_with_amounts_as_weights = {}
        for edge in list_edges:
            if edge in edges_with_amounts_as_weights:
                edges_with_amounts_as_weights[edge] += edge.amount
            else:
                edges_with_amounts_as_weights[edge] = edge.amount

        return edges_with_amounts_as_weights

    def show_edges_with_num_players_as_weights(self, list_edges):
        edges_with_num_players_as_weights = {}
        for edge in list_edges:
            if edge in edges_with_num_players_as_weights:
                edges_with_num_players_as_weights[edge] += 1
            else:
                edges_with_num_players_as_weights[edge] = 1
        return edges_with_num_players_as_weights
