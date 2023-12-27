from crawlers import *
from model import *

if len(file_name_headers) != len(directory_paths):
    print('Check news site membership numbers')
else:
    crawlCNN(date)
    crawlNewAtlas(date)
    crawlTheVerge(date)
    crawlTechCrunch()
    generate_summaries()
