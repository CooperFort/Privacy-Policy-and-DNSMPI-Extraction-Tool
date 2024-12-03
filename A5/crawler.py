import requests
from bs4 import BeautifulSoup
import re
import logging
import time

#Set up logging
logging.basicConfig(level=logging.INFO)

#Function to fetch privacy policy and dnsmpi link from a website
def find_privacy_and_dnsmpi(url, retries=3, delay=5):
	attempt = 0
	dnsmpi_links = {} #list to store DNSMPI-related links
	while attempt < retries:
		try:
			response = requests.get(url, timeout=30) #increased timeout
			if response.status_code != 200:
				logging.warning(f"Failed to fetch {url}: HTTP Status {response.status_code}")
				return None, None
			break #success, break out of the loop
		except requests.exceptions.Timeout:
			logging.warning(f"Timeout occurred while accessing {url}")
			attempt += 1
			if attempt < retries:
				logging.info(f"Retrying {url} in {delay} seconds...")
				time.sleep(delay)
			else:
				logging.error(f"Failed to fetch {url} after {retries} attempts.")
				return None, None
		except requests.exceptions.RequestException as e:
			logging.error(f"Request failed for {url}: {e}")
			return None, None

	soup = BeautifulSoup(response.txt, 'html.parser')

	#Search for the privacy policy link
	privacy_policy = None
	privacy_policy_link = soup.find('a', href=True, string=re.compiler(r'privacy', re.I))
	if privacy_policy_link:
		privacy_policy = privacy_policy_link['href']

	#search for DNSMPI-related links in anchor tags
	dnsmpi_keywords = [
		"do not sell", "privacy choices", "dnsmpi", "opt-out", "privacy preferences", "do not share", "data privacy", "cookies", "third-party",
		"advertising choices", "consumer rights", "manage your privacy", "control your data", "privacy settings", "user consent",
	 	"manage cookies", "ad preferences", "data protection", "cookie policy", "privacy rights", "privacy"
	]

	for a_tag in soup.find.all('a', href=True):
		link_text = a_tag.get_text(strip=True).lower()
		if any(keyword in link_text for keyword in dnsmpi_keywords):
			dnsmpi_links.append({
				"text": link_text,
				"url": a_tag['href']
			})

	# if no DNSMPI links are found, set to None
	dnsmpi_link = None
	if dnsmpi_links:
		dnsmpi_link = dnsmpi_links

	return privacy_policy, dnsmpi_link

# function to process a list of websites
def process_websites(input_file):
	results = []
	with open(input_file, 'r') as file:
		websites = file.readlines()

	for url in websites:
		url = url.strip()
		logging.info(f"Processing {url}")
		privacy_policy, dnsmpi_link = find_privacy_and_dnsmpi(url)

		#store the result in a dictionary
		results.append({
			'url': url,
			'privacy_policy': privacy_policy,
			'dnsmpi_links': dnsmpi_link
		})

	return results

# function to write the results to a JSON file
def write_results_to_json(results, output_file):
	import json
	with open(output_file, 'w') as outfile:
		json.dump(results, outfile, indent=4)

#main function to run the crawler
def main():
	input_file = 'websites.txt'
	output_file = 'scraped_data.json'

	# process websites and get privacy and DNSMPI links
	results = process_websites(input_file)

	#write the results to the json file
	write_results_to_json(results, output_file)
	logging.info(f"Results saved to {output_file}")

if __name__ == '__main__':
	main()
 
