import requests
from bs4 import BeautifulSoup
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
            header_div_tuple = (box.find_all("div", {"class": "table-header"}), box.find_all("div", {"class": "responsive-table"}))
            tuples.append(header_div_tuple)

        for t in tuples:
            if t[0] and t[1]:
                # print("=======================================================================================================")
                club = t[0][0].select("a", {"class": "vereinprofil_tooltip"})[1]
                club_name = club.get_text()
                club_id = club.get("id")
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

        print("------Finished calculating data for " + year_as_string + "----------")
    all_leagues.append(league)

edge_processor = EdgeProcessor()

for league in all_leagues:
    print("printing " + league.league_name + "......")
    for year in range(2017, 2019):
        print("=======showing the links for " + str(year))
        for link in league.transfers_for_year[year]:
            link.show_info()
