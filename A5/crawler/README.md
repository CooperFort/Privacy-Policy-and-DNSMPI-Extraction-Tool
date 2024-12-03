# Crawler - Privacy Policy and DNSMPI Link Scraper

This project contains a Python script (crawler.py) that scrapes privacy policy and 
DNSMPI (Do Not Sell My Personal Information) related links from a list of websites. 
The results are saved in a JSON format.

---

## Prerequisites

Before running the script, ensure that you have the following installed:

**Python 3**

**Required Python libraries**: requests, beautifulsoup4

To install the required libraries, you can use pip:

sudo apt install python3-requests python3-bs4

## Setup

Download the Website List: Prepare a text file (websites.txt) containing a list of websites you want to scrape. 

Each website should be on a new line in the file. For example:

`https://www.example1.com`

`https://www.example2.com`

**Crawler Script**: The script crawler.py is responsible for crawling each website in the websites.txt file 
to find the privacy policy and DNSMPI links. The script performs the following steps for each website:

- Fetches the website content.

- Searches for links related to privacy policies and DNSMPI (Do Not Sell My Personal Information).

- Saves the results in scraped_data.json.

## How to Run
Place the websites.txt file in the same directory as crawler.py, 
or adjust the script to point to the correct location of the file.

- Execute the script**:
    ```bash
    python3 crawler.py
    ```

- The results will be saved in scraped_data.json in the following format:

    ```bash
    [
        {
            "url": "https://www.example1.com",
            "privacy_policy": "https://www.example1.com/privacy-policy",
            "dnsmpi_links": [
                {
                    "text": "Do Not Sell My Personal Information",
                    "url": "https://www.example1.com/dnsmpi"
                }
            ]
        }
        
    ]
    ```

## How It Works
**Fetching Websites**: The script uses the requests library to fetch the HTML content of each website. 
The timeout for requests is set to 30 seconds to prevent the crawler from hanging if a website is slow to respond.

**Searching for Privacy Links**: The script looks for links that contain the word privacy in the anchor tag's text and 
stores the first found link as the privacy policy URL.

**Searching for DNSMPI Links**: The script looks for anchor tags with keywords like do not sell, privacy choices, dnsmpi, 
and similar terms in their text. If any of these keywords are found, the corresponding link is saved as a DNSMPI-related link.

**Retries and Timeouts**: The script will retry a website fetch up to 3 times if there is a timeout or a request failure. 
The retries are spaced out by a delay of 5 seconds.

**Input File**: By default, the script uses websites.txt as the input file for the list of websites. 
You can modify this by changing the input_file variable in the main function of the script.

**Keywords for DNSMPI**: The script uses a predefined list of keywords (do not sell, privacy choices, etc.) to search for DNSMPI-related links. 
You can add more keywords to the dnsmpi_keywords list if necessary.

## Troubleshooting

**Timeouts or Request Failures**: If a website takes too long to respond or if there are connection issues, 
the script will retry fetching the website up to 3 times. If the issue persists, it will log an error and skip the website.

**Missing Libraries**: If you see an error related to missing libraries, ensure that you have installed the required Python libraries 
(requests, beautifulsoup4) using apt install.

