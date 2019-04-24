import requests
import os
from bs4 import BeautifulSoup
from TransferLink import *
from LeagueURLConstants import *
from Club import *
from EdgeWeight import *
from League import *

from decimal import Decimal


class TransferDataScraperAndProcessor:

    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year
        self.headers = {'User-Agent':
                       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        # self.file_name = "../data/bundesliga.csv"
        self.url_start = "https://www.transfermarkt.us/"
        self.url_string_after_league_data = "/plus/?saison_id="
        self.url_end = "&s_w=&leihe=0&leihe=1&intern=0&intern=0"  # Include Loans and no club internal transfers(ChelseaU23 to Chelsea)
        self.all_transfers = [] #all transfer links
        self.all_loan_transfers = [] #all loan transfers
        self.all_leagues = [] #all leagues
        self.all_clubs = set() #all clubs. Each club object has a club id and name
        self.process_all_data(self.start_year, self.end_year)
        self.all_unique_edges = self.generate_unique_edges(self.all_transfers)
        self.all_unique_loan_edges = self.generate_unique_edges(self.all_loan_transfers)
        self.put_all_clubs_in_a_league()

    def process_amount(self, amount):
        if amount == "-" or amount == "Loan" or amount == "Free Transfer" or ("End of loan" in amount) or amount == "?":
            return 0
        else:
            wo_currency_amount = amount[amount.index('$') + 1:]
            multiplier_symbol = wo_currency_amount[len(wo_currency_amount) - 1]
            wo_currency_and_multiplier_amount = Decimal(wo_currency_amount[0:len(wo_currency_amount) - 1])
            if multiplier_symbol == 'm':
                amount = wo_currency_and_multiplier_amount * 1000000
            elif multiplier_symbol == 'k':
                amount = wo_currency_and_multiplier_amount * 1000
            # Remove Trailing Zeros after Decimal Point
            return amount.quantize(Decimal(1)) if amount == amount.to_integral() else amount.normalize()

    def get_transfer_type(self, amount):
        if "loan" in amount or "Loan" in amount:
            return "Loan"
        elif "Free Transfer" in amount:
            return "Free Transfer"
        else:
            return "Transfer"

    def process_all_data(self, start_year, end_year):
        for league_name in LeagueURLConstants.league_names_with_urls:
            print("=================================working on " + league_name + "=========================")
            league = League(league_name)
            # league_edges = []
            for year in range(start_year, end_year + 1):
                league.transfers_for_year[year] = []
                year_as_string = str(year)
                url_end = "&s_w=&leihe=0&leihe=1&intern=0"
                full_url = self.url_start + LeagueURLConstants.league_names_with_urls[league_name] + \
                           self.url_string_after_league_data + year_as_string + url_end
                print("calculating data for " + year_as_string + "..........")
                pageTree = requests.get(full_url, headers=self.headers)
                pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

                boxes = pageSoup.findAll("div", {"class": "box"})
                club_boxes = [box for box in boxes if box]

                # Remove the First 3 Box elements that are at the top of each page.
                club_boxes = club_boxes[3:]

                # table_headers = []

                tuples = []
                for box in club_boxes:
                    table_headers = box.find_all("div", {"class": "table-header"})

                    # Get only the Transfer out Boxes from Each Box.
                    responsive_table = box.find_all("div", {"class": "responsive-table"})[1::2]
                    header_div_tuple = (table_headers, responsive_table)
                    tuples.append(header_div_tuple)

                for t in tuples:
                    if t[0] and t[1]:
                        # print("=======================================================================================================")
                        source_team = t[0][0].select("a", {"class": "vereinprofil_tooltip"})
                        source_team_name = source_team[0].find("img").get("alt")
                        source_team_id = source_team[1].get("id")
                        transfers_out = t[1][0]
                        trs = transfers_out.find_all("tr")
                        source_team_club = Club(source_team_id, source_team_name)
                        if source_team_club not in self.all_clubs:
                            self.all_clubs.add(source_team_club)
                        for i in range(1, len(trs)):
                            tr = trs[i]
                            player_name = tr.find("span", {"class": "hide-for-small"}).get_text()
                            # Index 0 has market Value. Index 1 has Transfer Fee
                            player_amount = tr.find_all("td", {"class": "rechts"})[1].get_text()
                            player_pos = tr.find_all("td", {"class": "pos-transfer-cell"})[0].get_text()
                            target_team_details = tr.find("td", {"class": "no-border-links verein-flagge-transfer-cell"})
                            target_team = target_team_details.find("a", {"class": "vereinprofil_tooltip"})
                            target_team_name = tr.find("td", {"class": "no-border-rechts zentriert"}).find("img").get("alt")
                            transfer_type = self.get_transfer_type(player_amount)
                            processed_amount = self.process_amount(player_amount)
                            if target_team:
                                target_team_id = target_team.get("id")
                                retired_id = 123
                                without_club_id = 515
                                career_break_id = 2113
                                if target_team_id != retired_id or target_team_id != without_club_id or \
                                        target_team_id != career_break_id:
                                    link = TransferLink(source_team_id=source_team_id, target_team_id=target_team_id,
                                                        amount=processed_amount, player_pos=player_pos,
                                                        source_team_name=source_team_name,
                                                        target_team_name=target_team_name,
                                                        player_name=player_name, transfer_type=transfer_type)
                                    league.transfers_for_year[year].append(link)
                                    league.all_transfers.append(link)
                                    self.all_transfers.append(link)
                                    target_club = Club(target_team_id, target_team_name)
                                    if target_club not in self.all_clubs:
                                        self.all_clubs.add(target_club)
                                    if transfer_type == "Loan":
                                        self.all_loan_transfers.append(link)
                                        league.loan_tranfers.append(link)
                                    if source_team_club not in league.clubs:
                                        league.clubs.add(source_team_club)

                print("------Finished calculating data for " + year_as_string + "----------")
            self.all_leagues.append(league)

    def show_all_transfers_per_league(self, start_year, end_year):
        for league in self.all_leagues:
            print("printing " + league.league_name + "......")
            league.show_transfers_for(start_year, end_year)

    def show_all_teams(self):
        for league in self.all_leagues:
            league.show_all_teams_belonging_to_league()

    def generate_unique_edges(self, list_links):
        unique_edges = {}
        for edge in list_links:
            if edge in unique_edges:
                unique_edges[edge].increase_num_players()
                unique_edges[edge].increase_amount(edge.amount)
            else:
                unique_edges[edge] = EdgeWeight(1, edge.amount)
        return unique_edges

    def write_overall_output_with_weights_as_num_players(self):
        file_path = "../data/all_edges_num_players_as_weights_" + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "w") as file:
            file.write("source,target,weight\n")
            for edge in self.all_unique_edges:
                file.write(edge.source_team_id + ",")
                file.write(edge.target_team_id + ",")
                file.write(str(self.all_unique_edges[edge].num_players))
                file.write("\n")

    def write_overall_output_with_weights_as_total_cost(self):
        file_path = "../data/all_edges_total_cost_as_weights_" + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as file:
            file.write("source,target,weight\n")
            for edge in self.all_unique_edges:
                file.write(edge.source_team_id + ",")
                file.write(edge.target_team_id + ",")
                file.write(str(self.all_unique_edges[edge].total_amount))
                file.write("\n")

    def write_output_file_for_loans(self):
        file_path = "../data/overall_loan_network_" + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as file:
            file.write("source,target,weight\n")
            for edge in self.all_unique_loan_edges:
                file.write(edge.source_team_id + ",")
                file.write(edge.target_team_id + ",")
                file.write(str(self.all_unique_loan_edges[edge].num_players))
                file.write("\n")

    def put_all_clubs_in_a_league(self):
        other_league = League("Other")
        for club in self.all_clubs:
            belongs_to_known_leagues = False
            for league in self.all_leagues:
                if club in league.clubs:
                    belongs_to_known_leagues = True
                    break
            if not belongs_to_known_leagues:
                other_league.clubs.add(club)
        self.all_leagues.append(other_league)

    def write_out_node_communities(self):
        file_path = "../data/all_node_communities_"  + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as file:
            file.write("node,type\n")
            for league in self.all_leagues:
                for club in league.clubs:
                    file.write(str(club.club_id) + "," + league.league_name)
                    file.write("\n")

    def write_out_all_clubs_and_names(self):
        file_path = "../data/all_nodes_"  + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as file:
            file.write("node,label\n")
            for club in self.all_clubs:
                file.write(str(club.club_id) + "," + club.club_name)
                file.write("\n")




