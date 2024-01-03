from crawlers import *
from model import *
from uploader import *
import csv
import traceback

def main():
    # Check file structure
    if len(file_name_headers) != len(directory_paths):
        print('Check news site membership numbers')
        return  # Exit the function if the check fails

    # Crawling data
    crawlCNN(date)
    crawlNewAtlas(date)
    crawlTheVerge(date)
    crawlTechCrunch()

    # Generating summaries
    summaries = generate_summaries()
    
    # Writing summaries to CSV
    try:
        csv_file_path = base_directory / "NewsScrapes" / "Summaries" / f"Summaries_{date}.csv"
        
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for summary in summaries:
                writer.writerow(summary)
    except Exception as e:
        print(f"Error writing CSV: {e}")
        return  # Exit if CSV writing fails

    # Uploading to Google Drive
    try:
        drive_uploader()
    except Exception as e:
        print(f"Error uploading to Google Drive: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
