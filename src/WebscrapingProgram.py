from TransferDataScraperAndProcessor import *
import time

def main():
    start = time.time()
    # try:
    scraper_tool = TransferDataScraperAndProcessor(start_year=2000, end_year=2018)
    scraper_tool.write_out_all_clubs_and_names()
    scraper_tool.write_output_file_for_loans()
    scraper_tool.write_overall_output_with_weights(use_amount_as_weight=True)
    scraper_tool.write_overall_output_with_weights(use_amount_as_weight=False)
    scraper_tool.write_output_file_for_non_loan_transfers(use_amount_as_weight=True)
    scraper_tool.write_output_file_for_non_loan_transfers(use_amount_as_weight=False)
    scraper_tool.write_out_clubs_and_countries()

    # except Exception as e:
    #     print("=============something went wrong somewhere===============")
    #     print(e)
    end = time.time()
    print(str(end - start) + " seconds")


if __name__ == "__main__":
    main()

