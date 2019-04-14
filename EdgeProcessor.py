from Edge import Edge


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


# edges = []
# edge1 = Edge("team1", "team2", 129)
# edges.append(edge1)
# edge2 = Edge("team1", "team2", 300)
# edges.append(edge2)
# edge3 = Edge("team2", "team1", 200)
# edges.append(edge3)

# print(float("$3.2k"))

# weights = EdgeProcessor.show_edges_with_num_players_as_weights(edges)
# for w in weights:
#     print(str(w), weights[w])