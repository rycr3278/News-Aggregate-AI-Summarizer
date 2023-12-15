import requests
from bs4 import BeautifulSoup
import re

# Target URL
url = 'http://quotes.toscrape.com'

# Send GET request
response = requests.get(url)

# Parse HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data
quotes = soup.find_all('span', class_='text')


substr = '<span class="text" itemprop="text">�'
with open('readme.txt', 'w') as f:
    for quote in quotes:
        stripped_front = str(quote)[36:]
        stripped_back = stripped_front[:-8]
        f.write(stripped_back)
        f.write('\n')