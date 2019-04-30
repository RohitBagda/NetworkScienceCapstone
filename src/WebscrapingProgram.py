from TransferDataScraperAndProcessor import *
import time

def main():
    start = time.time()
    scraper_tool = TransferDataScraperAndProcessor(start_year=2018, end_year=2018)
    scraper_tool.write_out_all_clubs_and_leagues()
    scraper_tool.write_out_clubs_and_countries()
    scraper_tool.write_output_file_for_loans()
    scraper_tool.write_output_file_with_weights(include_loans=True)
    scraper_tool.write_output_file_with_weights(include_loans=False)
    end = time.time()
    print(str(end - start) + " seconds")


if __name__ == "__main__":
    main()

