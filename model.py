from transformers import pipeline, AutoModel
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



# Process each json file
for i in range(len(directory_paths)):
    json_file_path = os.path.join(directory_paths[i], file_name_headers[i] + date + '.json')
    
    with open(json_file_path, encoding='utf-8') as f:
        data = json.load(f)
        count = 0
        if isinstance(data, list):
            for item in data:
                count += 1
                if isinstance(item, dict) and 'maintext' in item and count <= 2:
                    # Check and truncate the text if it's too long
                    text = item['maintext'][:summarizer.tokenizer.model_max_length]
                    summary_text = summarizer(text, max_length=100, min_length=5, do_sample=False)[0]['summary_text']
                    hashtags = generate_hashtags(summary_text)
                    print(summary_text + ' ' + hashtags)