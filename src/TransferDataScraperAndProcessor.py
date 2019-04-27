import requests
import os
import csv
from bs4 import BeautifulSoup
from TransferLink import *
from LeagueURLConstants import *
from Club import *
from EdgeWeight import *
from League import *
from UniqueEdge import *
from decimal import Decimal


class TransferDataScraperAndProcessor:

    def __init__(self, start_year, end_year, should_include_loans=False):
        self.start_year = start_year
        self.end_year = end_year
        self.should_include_loans = should_include_loans
        self.headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        self.url_start = "https://www.transfermarkt.us/"
        self.url_string_after_league_data = "/plus/?saison_id="
        self.url_end = "&s_w=&leihe=0&leihe=1&intern=0&intern=0"  # Include Loans and no club internal transfers(ChelseaU23 to Chelsea)
        self.all_transfers = set()  # all transfer links
        self.all_loan_transfers = set()  # all loan transfers
        self.all_non_loan_transfers = set()
        self.all_leagues = set()  # all leagues
        self.all_clubs = set()  # all clubs. Each club object has a club id and name
        self.process_all_data(self.start_year, self.end_year)
        self.all_unique_edges = self.generate_unique_edges(self.all_transfers)
        self.all_unique_loan_edges = self.generate_unique_edges(self.all_loan_transfers)
        self.all_unique_non_loan_edges = self.generate_unique_edges(self.all_non_loan_transfers)
        self.put_all_clubs_in_a_league()

    def process_all_data(self, start_year, end_year):
        for league_name in LeagueURLConstants.league_names_with_urls:
            print("=================================working on " + league_name + "=========================")
            league = League(league_name)
            # league_edges = []
            for year in range(start_year, end_year + 1):
                league.transfers_for_year[year] = set()
                year_as_string = str(year)
                url_end = "&s_w=&leihe=0&leihe=1&intern=0"
                full_url = self.url_start + LeagueURLConstants.league_names_with_urls[league_name] + \
                           self.url_string_after_league_data + year_as_string + url_end
                print("calculating data for " + year_as_string + "..........")
                page_tree = requests.get(full_url, headers=self.headers)
                page_soup = BeautifulSoup(page_tree.content, 'html.parser')

                boxes = page_soup.findAll("div", {"class": "box"})
                club_boxes = [box for box in boxes if box]

                # Remove the First 3 Box elements that are at the top of each page.
                club_boxes = club_boxes[3:]

                tuples_out = []
                tuples_in = []
                for box in club_boxes:
                    table_headers = box.find_all("div", {"class": "table-header"})

                    # Get only the Transfer out Boxes from Each Box.
                    responsive_table_out_transfers = box.find_all("div", {"class": "responsive-table"})[1::2]
                    responsive_table_in_transfers = box.find_all("div", {"class": "responsive-table"})[0::1]
                    header_div_tuple_out = (table_headers, responsive_table_out_transfers)
                    tuples_out.append(header_div_tuple_out)

                    header_div_tuple_in = (table_headers, responsive_table_in_transfers)
                    tuples_in.append(header_div_tuple_in)

                for t in tuples_out:
                    if t[0] and t[1]:
                        # print("=====================================================================================")
                        source_team_details = self.get_header_team_details(t)
                        source_team_name = self.get_header_team_name(source_team_details)
                        source_team_id = self.get_header_team_id(source_team_details)
                        transfers_out = t[1][0]
                        trs = self.get_all_trs(transfers_out)
                        if "No departures" in trs[1].find("td").get_text():
                            continue
                        else:
                            source_team_club = Club(source_team_id, source_team_name)
                            if source_team_club not in self.all_clubs:
                                self.all_clubs.add(source_team_club)
                            for i in range(1, len(trs)):
                                tr = trs[i]
                                player_name = self.get_player_name(tr)
                                player_amount = self.get_player_amount(tr)
                                player_pos = self.get_player_position(tr)
                                target_team_details = self.get_tr_team_details(tr)
                                target_team = self.get_tr_team(target_team_details)
                                target_team_name = self.get_tr_team_name(tr)
                                transfer_type = self.get_transfer_type(player_amount)
                                processed_amount = self.process_amount(player_amount)

                                if target_team:
                                    target_team_id = self.get_tr_team_id(target_team)
                                    if self.valid_football_club(target_team_id):
                                        link = TransferLink(source_team_id=source_team_id,
                                                            target_team_id=target_team_id,
                                                            amount=processed_amount,
                                                            player_pos=player_pos,
                                                            source_team_name=source_team_name,
                                                            target_team_name=target_team_name,
                                                            player_name=player_name,
                                                            transfer_type=transfer_type,
                                                            year=year)
                                        league.transfers_for_year[year].add(link)
                                        league.all_transfers.add(link)
                                        self.all_transfers.add(link)
                                        target_club = Club(target_team_id, target_team_name)
                                        if target_club not in self.all_clubs:
                                            self.all_clubs.add(target_club)
                                        if transfer_type == "Loan":
                                            self.all_loan_transfers.add(link)
                                            league.loan_transfers.add(link)
                                        else:
                                            self.all_non_loan_transfers.add(link)
                                            league.non_loan_transfers.add(link)
                                        if source_team_club not in league.clubs:
                                            league.clubs.add(source_team_club)

                # -----------------Transfers IN ------------------------------------------------------------------------

                for t in tuples_in:
                    if t[0] and t[1]:
                        # print("=====================================================================================")
                        target_team_details = self.get_header_team_details(t)
                        target_team_name = self.get_header_team_name(target_team_details)
                        target_team_id = self.get_header_team_id(target_team_details)
                        transfers_in = t[1][0]
                        trs = self.get_all_trs(transfers_in)
                        if "No arrivals" in trs[1].find("td").get_text():
                            continue
                        else:
                            target_team_club = Club(target_team_id, target_team_name)
                            if target_team_club not in self.all_clubs:
                                self.all_clubs.add(target_team_club)
                            for i in range(1, len(trs)):
                                tr = trs[i]
                                player_name = self.get_player_name(tr)
                                player_amount = self.get_player_amount(tr)
                                player_pos = self.get_player_position(tr)
                                source_team_details = self.get_tr_team_details(tr)
                                source_team = self.get_tr_team(source_team_details)
                                source_team_name = self.get_tr_team_name(tr)
                                transfer_type = self.get_transfer_type(player_amount)
                                processed_amount = self.process_amount(player_amount)
                                if source_team:
                                    source_team_id = self.get_tr_team_id(source_team)
                                    if self.valid_football_club(source_team_id):
                                        link = TransferLink(source_team_id=source_team_id,
                                                            target_team_id=target_team_id,
                                                            amount=processed_amount,
                                                            player_pos=player_pos,
                                                            source_team_name=source_team_name,
                                                            target_team_name=target_team_name,
                                                            player_name=player_name,
                                                            transfer_type=transfer_type,
                                                            year=year)
                                        league.transfers_for_year[year].add(link)
                                        league.all_transfers.add(link)
                                        self.all_transfers.add(link)
                                        source_club = Club(source_team_id, source_team_name)
                                        if source_club not in self.all_clubs:
                                            self.all_clubs.add(source_club)
                                        if transfer_type == "Loan":
                                            self.all_loan_transfers.add(link)
                                            league.loan_transfers.add(link)
                                        else:
                                            self.all_non_loan_transfers.add(link)
                                            league.non_loan_transfers.add(link)
                                        if target_team_club not in league.clubs:
                                            league.clubs.add(target_team_club)

                print("------Finished calculating data for " + year_as_string + "----------")
            self.all_leagues.add(league)

    def get_header_team_details(self, t):
        return t[0][0].select("a", {"class": "vereinprofil_tooltip"})

    def get_header_team_name(self, team_details):
        return team_details[0].find("img").get("alt")

    def get_header_team_id(self, team_details):
        return team_details[1].get("id")

    def get_all_trs(self, transfers):
        return transfers.find_all("tr")

    def get_player_name(self, tr):
        return tr.find("span", {"class": "hide-for-small"}).get_text()

    def get_player_amount(self, tr):
        # Index 0 has market Value. Index 1 has Transfer Fee
        return tr.find_all("td", {"class": "rechts"})[1].get_text()

    def get_player_position(self, tr):
        return tr.find_all("td", {"class": "pos-transfer-cell"})[0].get_text()

    def get_tr_team_details(self, tr):
        return tr.find("td", {"class": "no-border-links verein-flagge-transfer-cell"})

    def get_tr_team(self, team_details):
        return team_details.find("a", {"class": "vereinprofil_tooltip"})

    def get_tr_team_name(self, tr):
        return tr.find("td", {"class": "no-border-rechts zentriert"}).find("img").get("alt")

    def get_tr_team_id(self, team):
        return team.get("id")

    def process_amount(self, amount):
        # if amount == "-" or amount == "Loan" or amount == "Free Transfer" or ("End of loan" in amount) or amount == \
        #         "?" or amount == "" or amount == "draft":
        #     return 0
        if '$' not in amount:
            return 0
        else:
            wo_currency_amount = amount[amount.index('$') + 1:]
            multiplier_symbol = wo_currency_amount[len(wo_currency_amount) - 1]
            wo_currency_and_multiplier_amount = Decimal(wo_currency_amount[0:len(wo_currency_amount) - 1])
            if multiplier_symbol == 'm':
                amount = wo_currency_and_multiplier_amount * 1000000
            elif multiplier_symbol == 'k':
                amount = wo_currency_and_multiplier_amount * 1000
            else:
                amount = Decimal(wo_currency_amount)
            # Remove Trailing Zeros after Decimal Point
            return amount.quantize(Decimal(1)) if amount == amount.to_integral() else amount.normalize()

    def get_transfer_type(self, amount):
        if ("loan" in amount or "Loan" in amount) and "end of" not in amount.lower():
            return "Loan"
        elif "Free Transfer" in amount:
            return "Free Transfer"
        else:
            return "Transfer"

    def valid_football_club(self, team_id):
        retired_id = 123
        without_club_id = 515
        career_break_id = 2113
        if team_id != retired_id or team_id != without_club_id or team_id != career_break_id:
            return True
        return False

    def show_all_transfers_per_league(self, start_year, end_year):
        for league in self.all_leagues:
            print("printing " + league.league_name + "......")
            league.show_transfers_for(start_year, end_year)

    def show_all_teams(self):
        for league in self.all_leagues:
            league.show_all_teams_belonging_to_league()

    def generate_unique_edges(self, set_links):
        unique_edges = {}
        for link in set_links:
            unique_edge = UniqueEdge(link.source_team_id, link.target_team_id)
            if unique_edge in unique_edges:
                unique_edges[unique_edge].increase_num_players()
                unique_edges[unique_edge].increase_amount(link.amount)
            else:
                unique_edge = UniqueEdge(link.source_team_id, link.target_team_id)
                unique_edges[unique_edge] = EdgeWeight(1, link.amount)
        return unique_edges

    def write_overall_output_with_weights(self, use_amount_as_weight=True):
        if use_amount_as_weight:
            file_path_start = "../data/all_edges_total_cost_as_weights_"
        else:
            file_path_start = "../data/all_edges_num_players_as_weights_"
        file_path = file_path_start +  str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["source", "target", "weight"])
            for edge in self.all_unique_edges:
                if use_amount_as_weight:
                    weight = str(self.all_unique_edges[edge].total_amount)
                else:
                    weight = str(self.all_unique_edges[edge].num_players)
                writer.writerow([edge.source_id, edge.target_id, weight])

    def write_output_file_for_loans(self):
        file_path = "../data/overall_loan_network_" + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["source", "target", "weight"])
            for edge in self.all_unique_loan_edges:
                writer.writerow([edge.source_id, edge.target_id, str(self.all_unique_loan_edges[edge].num_players)])

    def write_output_file_for_non_loan_transfers(self, use_amount_as_weight=True):
        if use_amount_as_weight:
            file_path_start = "../data/overall_non_loan_network_weights_as_total_cost"
        else:
            file_path_start = "../data/overall_non_loan_network_weights_as_num_players"
        file_path = file_path_start + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["source", "target", "weight"])
            for edge in self.all_unique_non_loan_edges:
                if use_amount_as_weight:
                    weight = str(self.all_unique_edges[edge].total_amount)
                else:
                    weight = str(self.all_unique_edges[edge].num_players)
                writer.writerow([edge.source_id, edge.target_id, weight])

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
        self.all_leagues.add(other_league)


    def write_out_all_clubs_and_names(self):
        file_path = "../data/all_nodes_"  + str(self.start_year) + "_" + str(self.end_year) + ".csv"
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(["id", "Label", "Modularity Class"])
            for league in self.all_leagues:
                print(league.league_name + ", " + str(len(league.clubs)))
                for club in league.clubs:
                    writer.writerow([str(club.club_id), club.club_name, league.league_name])
