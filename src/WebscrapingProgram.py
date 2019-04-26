from TransferDataScraperAndProcessor import *


def main():
    scraper_tool = TransferDataScraperAndProcessor(start_year=2017, end_year=2018)
    scraper_tool.write_out_all_clubs_and_names()
    scraper_tool.write_output_file_for_loans()
    scraper_tool.write_out_node_communities()
    scraper_tool.write_overall_output_with_weights_as_num_players()
    scraper_tool.write_overall_output_with_weights_as_total_cost()


if __name__ == "__main__":
    main()

