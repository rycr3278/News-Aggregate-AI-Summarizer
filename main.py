import requests
from bs4 import BeautifulSoup

# Target URL
url = 'http://quotes.toscrape.com'

# Send GET request
response = requests.get(url)

# Parse HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data
quotes = soup.find_all('span', class_='text')
for quote in quotes:
    print(quote.text)
