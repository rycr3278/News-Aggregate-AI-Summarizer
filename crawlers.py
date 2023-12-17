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

def crawlMITReview(date):
	
	# Base URL of the site to crawl
	base_url = 'https://www.technologyreview.com'

		# Send GET request
	response = requests.get(base_url)

	# Parse HTML content
	soup = BeautifulSoup(response.content, 'html.parser')

	# Find all article elements
	articles = soup.find_all('h3', class_='homepageStoryCard__hed--92c78a74bbc694463e43e32aafbbdfd7')

	# Write to file with UTF-8 encoding
	with open('MIT Review_' + date + '.txt', 'w', encoding='utf-8') as f:
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
				date_element = article_soup.find('div', class_="contentArticleHeader__publishDate--7eebb1699e639d6cdf75ced975c26010")
				author_element = article_soup.find('a', class_="byline__name--0f13a06758d50e60b13981eba38e67b0 byline__storyPage--0ea6f2bef44ac9c70f6581d3d7f21b41")
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
				f.write(author[:-12])
				f.write('\n')
				f.write(content[:-472])
				f.write('\n\n')
			else:
				# Write only the headline if no link is found
				f.write(headline)
				f.write('\n\n')

def crawlNewAtlas(date):
	base_url = 'https://www.newatlas.com'

	# Send GET request
	response = requests.get(base_url)

	# Parse HTML content
	soup = BeautifulSoup(response.content, 'html.parser')

	# Find all article elements
	articles = soup.find_all('a', class_='Link')

	processed_links = []
	
	# Write to file with UTF-8 encoding
	with open('New Atlas_' + date + '.txt', 'w', encoding='utf-8') as f:
		for article in articles:
			# Extract the href attribute
			link = article.get('href')
			if link:
				# Check if the link is a full URL or a relative path
				full_link = link if link.startswith('http') else base_url + link

				if full_link in processed_links:
					continue
				else:

					# Request the article page
					try:
						article_response = requests.get(full_link)
						article_soup = BeautifulSoup(article_response.content, 'html.parser')

						# Initialize variables
						headline = 'No headline'
						date = 'No date'
						author = 'No author'
						content = ''

						# Try to extract headline, date, author, and content
						headline_tag = article_soup.find('h1', class_='ArticlePage-headline')  
						if headline_tag:
							headline = headline_tag.get_text(strip=True)
						else:
							headline = 'No headline found'

						date_element = article_soup.find('div', class_="ArticlePage-datePublished")
						if date_element:
							date = date_element.get_text(strip=True)

						# Using regular expression to match the author profile URL pattern
						author_elements = article_soup.find_all('a', href=re.compile(r'/author/'))
						for author_element in author_elements:
							# Extract author name from the text of the first matching element
							author_name = author_element.get_text(strip=True)
							if author_name:
								author = author_name
								break
						else:
							author = 'No author found'


						content_elements = article_soup.find_all('p')
						if content_elements:
							content = ' '.join([p.get_text(strip=True) for p in content_elements])

						if headline != 'No headline found':
							
							# Write to file
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
							processed_links.append(full_link)
							

					except requests.exceptions.RequestException as e:
						print(f"Error requesting {full_link}: {e}")




