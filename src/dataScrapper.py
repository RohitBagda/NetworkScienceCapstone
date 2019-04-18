import requests
from bs4 import BeautifulSoup
import pandas as pd
from TransferLink import *
from EdgeProcessor import *
from DataOrganiser import *

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

url = "https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=2018&s_w=&leihe=0&intern=0&intern=1"
url2 = "https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id=2018&s_w=&leihe=0&leihe=1&intern=0&intern=1"
all_edges = []
file_name = "../data/bundesliga.csv"
url_start = "https://www.transfermarkt.co.uk/"
url_string_after_league_data = "/plus/?saison_id="
url_end = "&s_w=&leihe=0&leihe=1&intern=0&intern=1"
league_name_url_matcher = LeagueNameAndUrlMatcher()
all_leagues = []
for league_name in league_name_url_matcher.league_name_url_map:
    print("=================================working on " + league_name + "...")
    league = League(league_name)
    # league_edges = []
    for year in range(2017, 2019):
        league.transfers_for_year[year] = []
        # url_start = "https://www.transfermarkt.co.uk/bundesliga/transfers/wettbewerb/L1/plus/?saison_id="
        # url_start = "https://www.transfermarkt.co.uk/premier-league/transfers/wettbewerb/GB1/plus/?saison_id="
        year_as_string = str(year)
        url_end = "&s_w=&leihe=0&leihe=1&intern=0&intern=1"
        full_url = url_start + league_name_url_matcher.league_name_url_map[league_name] + \
                   url_string_after_league_data + year_as_string + url_end
        print("calculating data for " + year_as_string + "..........")
        pageTree = requests.get(full_url, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

        boxes = pageSoup.findAll("div", {"class": "box"})
        club_boxes = [box for box in boxes if box]

        table_headers = []
        table_div = []
        selling_clubs = []

        tuples = []
        for box in club_boxes:
            # if box:
            #     club = box.find_all("div", {"class": "table-header"})
            #     if club:
            #         print(club)
            #     club_name = club.select("a", {"class": "vereinprofil_tooltip"})[1].get_text()
            #     # print(club_name)
            #     club_details = box.find_all("div", {"class": "responsive-table"})
            #     if club_details:
            #         out_transfers = club_details[1]
            #         print(out_transfers)
            #         print("=================================")

            # table_headers.append(box.find_all("div", {"class": "table-header"}))
            # table_div.append(box.find_all("div", {"class": "responsive-table"}))
            header_div_tuple = (box.find_all("div", {"class": "table-header"}), box.find_all("div", {"class": "responsive-table"}))
            tuples.append(header_div_tuple)
        #
        # table_headers = table_headers[2:]
        # for table_header in table_headers:
        #     if table_header:
        #         selling_club = table_header[0].select("a", {"class": "vereinprofil_tooltip"})[1].get_text()
        #         print(selling_club)

        for t in tuples:
            if t[0] and t[1]:
                # print("=======================================================================================================")
                club = t[0][0].select("a", {"class": "vereinprofil_tooltip"})[1]
                club_name = club.get_text()
                club_id = club.get("id")
                # print(club_id)
                # club_id = t[0][0].select("a", )
                # print(club_name + "\n" + "-------------")
                table_div = t[1]
                if table_div:
                    transfers_out = t[1][1]
                    trs = transfers_out.find_all("tr")
                    for i in range(1, len(trs)):
                        tr = trs[i]
                        player_name = tr.find("span", {"class": "hide-for-small"}).get_text()
                        target_team_details = tr.find("td", {"class": "no-border-links verein-flagge-transfer-cell"})
                        target_team = target_team_details.find("a", {"class": "vereinprofil_tooltip"})
                        if target_team:
                            target_team_id = target_team.get("id")
                            link = TransferLink(source_team=club_id, target_team=target_team_id)
                            league.transfers_for_year[year].append(link)
                            # league_edges.append(edge)
                            # all_edges.append(edge)
        print("------Finished calculating data for " + year_as_string + "----------")
    all_leagues.append(league)
    # league_edge_processor = EdgeProcessor()
    # league_weights

edge_processor = EdgeProcessor()

for league in all_leagues:
    print("printing " + league.league_name + "......")
    for year in range(2017, 2019):
        print("=======showing the links for " + str(year))
        for link in league.transfers_for_year[year]:
            link.show_info()
        # all_links_for_year = edge_processor.show_edges_with_num_players_as_weights(list_edges=league.edges_for_each_year[year])
        # for link in all_links_for_year:
        #     print(link.source_team, link.target_team, all_links_for_year[link])

                    # print(player_name + "," + str(target_team))
                # all_transfers_out = transfers_out.find_all("span", {"class": "hide-for-small"})
                # ages = transfers_out.find_all("td", {"class": "zentriert alter-transfer-cell"})
                # for transfer_out in all_transfers_out:
                #     print(transfer_out.get_text())

            # print("===================================================================================================")
# edge_processor = EdgeProcessor()
# weights = edge_processor.show_edges_with_num_players_as_weights(list_edges=edges)
# with open(file_name, "w+") as file:
#     file.truncate()
#     for w in weights:
#         file.write(str(w) + "," + str(weights[w]) + "\n")

# for w in weights:
#     print(str(w) + "," + str(weights[w]))
# print(len(edges))
# for edge in edges:
#     print(str(edge))


# table_headers = table_headers[2:]
# table_div = [table for table in table_div if table]
#
# table_rows = []
# table_data = []
# for thing in table_div[0]:
#     table_rows.append(thing.find_all("tr"))
#     for row in table_rows[0]:
#         table_data.append(row.find_all("td"))
#
# for
# table_data = [data for data in table_data if data]
# for data in table_data:
#     print(data[0].find("span", {"class": "hide-for-small"}).get_text())
#     print(data[1].get_text())
#     print(data[2])
#     print("+++++++++++++")
# for table_header in table_headers:
#     if table_header:
#         selling_clubs.append(table_header[0].select("a", {"class": "vereinprofil_tooltip"})[1].get_text())
#
# print(selling_clubs)
# new_table = pd.DataFrame(columns=range(0, 7), index=[0])  # I know the size



# for each_table_div in table_div:
# row_marker = 0
# for thing in table_div[0]:
#     for row in thing.find_all("tr"):
#         column_marker = 0
#         columns = row.find_all('td')
#         for column in columns:
#             new_table.iat[row_marker, column_marker] = column.get_text()
#             column_marker += 1

# print(new_table)