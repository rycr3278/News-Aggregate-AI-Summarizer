from transformers import pipeline
from crawlers import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Initialize the summarizer
summarizer = pipeline("summarization")

# Function to generate hashtags from a summary
def generate_hashtags(text, n_hashtags=2):
    # Tokenize and lower the case
    tokens = word_tokenize(text.lower())

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]

    # Select the first 'n' tokens as hashtags
    hashtags = ['#' + word for word in tokens[:n_hashtags]]
    return ' '.join(hashtags)

def generate_summaries():
    summaries = []
    for i in range(len(directory_paths)):
        # Convert the directory path to a pathlib.Path object
        directory_path = Path(directory_paths[i])
        
        # Construct the filename
        filename = f"{file_name_headers[i]}{date}.json"
        
        # Use the / operator to join the directory path and the filename
        json_file_path = directory_path / filename
        with open(json_file_path, encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get('maintext'):
                        text = item['maintext'][:summarizer.tokenizer.model_max_length]
                        summary_text = summarizer(text, max_length=100, min_length=5, do_sample=False)[0]['summary_text']
                        hashtags = generate_hashtags(summary_text)
                        summaries.append([summary_text, hashtags, item['url']])
    return summaries
