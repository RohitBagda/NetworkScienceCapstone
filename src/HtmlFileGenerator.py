import requests
from LeagueURLConstants import *
import time
import os


def generate_html_files_for_year_and_league(start_year, end_year):
    headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    for year in range(start_year, end_year + 1):
        year_as_string = str(year)
        for league_name in LeagueURLConstants.league_names_with_urls:
            print("Generating HTML for " + league_name +
                  " " + year_as_string)
            generated_file_name = "../html/" + str(year) + league_name + ".html"
            url_start = "https://www.transfermarkt.us/"
            url_end = "&s_w=&leihe=0&leihe=1&intern=0&intern=0"
            string_after_league_data = "/plus/?saison_id="
            full_url = url_start + LeagueURLConstants.league_names_with_urls[league_name] + \
                       string_after_league_data + year_as_string + url_end
            page_tree = requests.get(full_url, headers=headers)
            if os.path.exists(generated_file_name):
                os.remove(generated_file_name)
            with open(generated_file_name, "wb") as file:
                file.write(page_tree.content)


def generate_html_files_for_most_expensive_transfer(start_year, end_year):
    headers = {'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    for year in range(start_year, end_year + 1):
        year_as_string = str(year)
        print("Generating File for Most Expensive Transfer HTML file for Year " + year_as_string)
        generated_file_name = "../html/" + str(year) + "MostExpensiveTransfer.html"
        url_start = "https://www.transfermarkt.us/transfers/transferrekorde/statistik/top/plus/1/galerie/0" \
                    "?saison_id="
        url_end = "&land_id=&ausrichtung=&spielerposition_id=&altersklasse=&leihe=&w_s="
        full_url = url_start + year_as_string + url_end
        page_tree = requests.get(full_url, headers=headers)
        if os.path.exists(generated_file_name):
            os.remove(generated_file_name)
        with open(generated_file_name, "wb") as file:
            file.write(page_tree.content)
def main():
    start = time.time()
    # generate_html_files_for_year_and_league(2000, 2018)
    generate_html_files_for_most_expensive_transfer(2000, 2018)
    end = time.time()
    print(end - start, " seconds")


if __name__ == "__main__":
    main()