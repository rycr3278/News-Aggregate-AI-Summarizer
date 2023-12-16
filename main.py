import requests
from bs4 import BeautifulSoup
import re
import datetime

today = datetime.date.today()
date = today.strftime("%m/%d/%y").replace('/', '')

def crawlCNN(date):
    
	# Base URL of the site to crawl
	base_url = 'https://www.cnn.com'

	# Specific section to scrape
	section_url = '/business/tech'

	# Send GET request
	response = requests.get(base_url + section_url)

	# Parse HTML content
	soup = BeautifulSoup(response.content, 'html.parser')

	# Find all article elements
	articles = soup.find_all('span', class_='container__headline-text')

	# Write to file with UTF-8 encoding
	with open('CNN Tech_' + date + '.txt', 'w', encoding='utf-8') as f:
		for article_span in articles:
			headline = article_span.get_text(strip=True)

			# Find the parent <a> tag of the <span> tag
			link_tag = article_span.find_parent('a', href=True)

			if link_tag:
				link = link_tag['href']
				full_link = base_url + link if link.startswith('/') else link

				# Request the article page
				article_response = requests.get(full_link)
				article_soup = BeautifulSoup(article_response.content, 'html.parser')

				# Extract date, author, and content (selectors need to be adjusted)
				date_element = article_soup.find('div', class_='timestamp')
				author_element = article_soup.find('span', class_='byline__name')
				content_elements = article_soup.find_all('p')

				date = date_element.get_text(strip=True) if date_element else 'No date'
				author = author_element.get_text(strip=True) if author_element else 'No author'
				content = ' '.join([p.get_text(strip=True) for p in content_elements])

				f.write(headline)
				f.write('\n')
				f.write(full_link)
				f.write('\n')
				f.write(date)
				f.write('\n')
				f.write(author)
				f.write('\n')
				f.write(content)
				f.write('\n\n')
			else:
				# Write only the headline if no link is found
				f.write(headline)
				f.write('\n\n')

crawlCNN(date)