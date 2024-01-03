import requests
from bs4 import BeautifulSoup
import datetime
import os
from pathlib import Path
from newsplease import NewsPlease
import json

# This will automatically find the path to the Documents folder
base_directory = Path.home() / "Documents"

# Folders for each crawling function
CNNTech = "CNN_Tech_Articles"
NewAtlas = "New_Atlas"
TheVerge = "The_Verge"
TechCrunch = "TechCrunch"

today = datetime.date.today()
date = today.strftime("%m/%d/%y").replace('/', '')

# Full paths for each folder
CNN_directory_path = base_directory / "NewsScrapes" / CNNTech
NewAtlas_directory_path = base_directory / "NewsScrapes" / NewAtlas
TheVerge_directory_path = base_directory / "NewsScrapes" / TheVerge
TechCrunch_directory_path = base_directory / "NewsScrapes" / TechCrunch

# List of paths for easy iteration
directory_paths = [CNN_directory_path, NewAtlas_directory_path, TheVerge_directory_path, TechCrunch_directory_path]

# List of file name headers for easy iteration
file_name_headers = ['CNN_', 'NewAtlas_', 'TheVerge_', 'TechCrunch_']

# Create the directories if they do not exist
for path in directory_paths:
	if not os.path.exists(path):
		os.makedirs(path)

def get_request(base_url, section_url, article_tag, identifier):
	# Send GET request
	response = requests.get(base_url + section_url)
	# Parse HTML content
	soup = BeautifulSoup(response.content, 'html.parser')
	# Find all article elements
	articles = soup.find_all(article_tag, class_ = identifier)

	return articles

	headline = article_span.get_text(strip=True)
	article_data = []

	# Find the parent <a> tag of the <span> tag
	link_tag = article_span.find_parent('a', href=True)

	if link_tag:
		link = link_tag['href']
		full_link = base_url + link if link.startswith('/') else link

		# Request the article page
		article_response = requests.get(full_link)
		article_soup = BeautifulSoup(article_response.content, 'html.parser')

		# Extract date, author, and content (selectors need to be adjusted)
		date_element = article_soup.find(date_tag, class_=date_identifier)
		author_element = article_soup.find(author_tag, class_=author_identifier)
		content_elements = article_soup.find_all(content_identifier)

		date = date_element.get_text(strip=True) if date_element else 'No date'
		author = author_element.get_text(strip=True) if author_element else 'No author'
		content = ' '.join([p.get_text(strip=True) for p in content_elements])

		article_data.append(str(headline))
		article_data.append(str(full_link))
		article_data.append(str(date))
		article_data.append(str(author))
		article_data.append(str(content))
		
	else:
		# Write only the headline if no link is found
		article_data.append(str(headline))
	
	return article_data
	
def crawlCNN(date):
	
	base_url = 'https://www.cnn.com'
	section_url = '/business/tech'

	articles = get_request(base_url, section_url, 'span', 'container__headline-text')

	all_articles_data = []

	for article in articles:
		# Find the parent <a> tag of the <span> tag
		link_tag = article.find_parent('a', href=True)

		if link_tag:
			link = link_tag['href']
			full_link = base_url + link if link.startswith('/') else link
    
		story = NewsPlease.from_url(full_link)

		article_data = {
			'title': story.title,
			'url': story.url,
			'date_publish': story.date_publish.isoformat() if story.date_publish else None,
			'authors': story.authors,
			'maintext': story.maintext
		}

		all_articles_data.append(article_data)

	json_file_path = os.path.join(CNN_directory_path, 'CNN_' + date + '.json')
	with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
		json.dump(all_articles_data, jsonfile, ensure_ascii=False, indent=4)
				
def crawlNewAtlas(date):
	base_url = 'https://www.newatlas.com'
	section_url = ''
	
	articles = get_request(base_url, section_url, 'a', 'Link')
	all_articles_data = []

	for article in articles:
		link = article.get('href')
		if link:
				
				full_link = base_url + link if link.startswith('/') else link
    
		story = NewsPlease.from_url(full_link)

		article_data = {
			'title': story.title,
			'url': story.url,
			'date_publish': story.date_publish.isoformat() if story.date_publish else None,
			'authors': story.authors,
			'maintext': story.maintext
		}

		all_articles_data.append(article_data)

	json_file_path = os.path.join(NewAtlas_directory_path, 'NewAtlas_' + date + '.json')
	with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
		json.dump(all_articles_data, jsonfile, ensure_ascii=False, indent=4)

def crawlTheVerge(date):
	
	base_url = 'https://www.theverge.com'
	section_url = '/tech'

	# Find all article elements
	class1_articles = get_request(base_url, section_url, 'a', 'after:absolute after:inset-0 group-hover:shadow-highlight-franklin dark:group-hover:shadow-highlight-blurple')
	class2_articles = get_request(base_url, section_url, 'a', 'after:absolute after:inset-0 group-hover:shadow-underline-blurple dark:group-hover:shadow-underline-franklin')
	articles = class1_articles + class2_articles

	all_articles_data = []

	for article in articles:
		link = article.get('href')
		if link:
			full_link = base_url + link if link.startswith('/') else link
    
		story = NewsPlease.from_url(full_link)

		article_data = {
			'title': story.title,
			'url': story.url,
			'date_publish': story.date_publish.isoformat() if story.date_publish else None,
			'authors': story.authors,
			'maintext': story.maintext
		}

		all_articles_data.append(article_data)

	json_file_path = os.path.join(TheVerge_directory_path, 'TheVerge_' + date + '.json')
	with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
		json.dump(all_articles_data, jsonfile, ensure_ascii=False, indent=4)

def crawlTechCrunch():
	base_url = 'https://techcrunch.com/'
	articles = get_request(base_url, '', 'a', 'post-block__title__link')

	all_articles_data = []

	for article in articles:
		link = article.get('href')
		story = NewsPlease.from_url(link)

		article_data = {
			'title': story.title,
			'url': story.url,
			'date_publish': story.date_publish.isoformat() if story.date_publish else None,
			'authors': story.authors,
			'maintext': story.maintext
		}

		all_articles_data.append(article_data)

	json_file_path = os.path.join(TechCrunch_directory_path, 'TechCrunch_' + date + '.json')
	with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
		json.dump(all_articles_data, jsonfile, ensure_ascii=False, indent=4)
