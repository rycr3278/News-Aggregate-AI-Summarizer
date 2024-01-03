# README.md for Web Scraper Project

## Overview

This project is a comprehensive web scraping and summarization tool designed to collect, summarize, and upload news articles from various tech news websites. The tool crawls specified sections of each website, extracts article data, generates summaries, and then uploads these summaries to Google Drive.

## Technologies Used

- **Python**: The primary programming language used.
- **Requests & BeautifulSoup**: For web scraping functionalities.
- **NewsPlease**: An integrated web scraping and information extraction library.
- **NLTK**: For text processing and generating hashtags from summaries.
- **PyDrive**: To handle file uploads to Google Drive.
- **Transformers (from Hugging Face)**: For leveraging pre-trained models to generate summaries of the articles.

## Functionality

1. **Crawling**: The tool crawls specified sections of CNN Tech, New Atlas, The Verge, and TechCrunch, collecting article data including titles, URLs, publication dates, authors, and main text content.
2. **Summarization**: Using the Transformers pipeline, it generates concise summaries of the articles.
3. **Hashtag Generation**: It then processes these summaries to generate relevant hashtags.
4. **Data Storage**: The summaries along with the hashtags and URLs are stored in a CSV file.
5. **Uploading**: Finally, the CSV file is uploaded to Google Drive for accessibility and storage.

## Setup Instructions

1. **Environment Setup**:
   - Ensure Python is installed on your machine.
   - Install necessary Python packages:
     ```
     pip install requests beautifulsoup4 news-please nltk pydrive transformers
     ```
   - Run the NLTK downloader to get the required datasets:
     ```
     python -m nltk.downloader popular
     ```

2. **Google Drive API Setup**:

    To use the uploading feature of this script, you need to set up your own Google Drive API credentials. Follow these steps to obtain your `client_secrets.json` file:

    1. **Create a Google Cloud Project**:
      - Go to the [Google Cloud Console](https://console.cloud.google.com/).
      - Click on "Select a project" > "NEW PROJECT".
      - Enter a project name and click "CREATE".

    2. **Enable the Google Drive API**:
      - In the dashboard of your new project, navigate to "APIs & Services" > "Dashboard".
      - Click on "+ ENABLE APIS AND SERVICES".
      - Search for "Google Drive API" and enable it for your project.

    3. **Configure OAuth Consent Screen**:
      - In the sidebar under "APIs & Services", select "OAuth consent screen".
      - Choose the User Type (usually "External") and click "CREATE".
      - Fill out the required fields (app name, user support email, etc.).
      - Click "SAVE AND CONTINUE" until you can click "BACK TO DASHBOARD".

    4. **Create OAuth 2.0 Client IDs**:
      - In the sidebar, select "Credentials".
      - Click "+ CREATE CREDENTIALS" and choose "OAuth client ID".
      - For "Application type", select "Web application".
      - Add "Authorized redirect URIs" (e.g., `http://localhost:8080/`, as per your `client_secrets.json` file).
      - Click "CREATE" and note your client ID and client secret.

    5. **Download the `client_secrets.json` File**:
      - In the "Credentials" page, find your OAuth 2.0 Client IDs.
      - Click on the download button (a small download icon) to the right of your Web Client ID.
      - This will download your `client_secrets.json` file.

    6. **Place the File in Your Project Directory**:
      - Copy the `client_secrets.json` file into the root directory of the web scraper project.

    7. **First-Time Authorization**:
      - Run `python main.py` in your terminal.
      - The script will open a new window in your default web browser.
      - Log in with your Google account and grant the necessary permissions.
      - This process will create a token file that allows the script to access your Google Drive.

    Remember, these credentials are unique to your Google account and should not be shared.

3. **Configuring the Client Secrets File**:

    - Rename the downloaded `client_secrets.json` file to `client_secrets_sample.json`.
    - Open `client_secrets_sample.json` and replace the placeholder values with your actual Google Cloud project's OAuth credentials.
    - After replacing the values, rename `client_secrets_sample.json` to `client_secrets.json`.
    - Ensure that the renamed `client_secrets.json` file is placed in the root directory of your project.
    - Add `client_secrets.json` to your `.gitignore` file to prevent it from being tracked by Git and pushed to GitHub.


4. **Running the Program**:
   - Navigate to the project directory in your terminal or command prompt.
   - Run the script using:
     ```
     python main.py
     ```
   - The script will automatically crawl, process, and upload the data. Check the terminal for any error messages or confirmation of successful operations.

## Usage Notes

- The script uses the current date to name the JSON and CSV files, so running it on different days will create new sets of files.
- Check your Google Drive for the uploaded CSV files named in the format `Summaries_MMDDYY.csv`.
- Modify the crawler functions if you need to target different websites or webpage structures.

---
