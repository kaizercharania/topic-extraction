from topic_extraction_functions import topic_extraction

topic_extraction.url = str(input('Please Enter the URL: '))
if not(topic_extraction.url.startswith('http')):
    raise ValueError("Please provide the url in the format:'http://xyz.com'")
try:
    topic_extraction.num_topic = int(input("Number of Topics(provide a integer): ") or 5)
except ValueError:
    input = 5
try:
    topic_extraction.topic_length =  int(input("length of topic(provide a number): ") or 3)
except ValueError:
    input = 3 
response = topic_extraction.get_url_response(topic_extraction.url)
page_text =  topic_extraction.get_page_text(response)
removed_punct = topic_extraction.remove_punctuation(page_text)
filtered_words = topic_extraction.remove_stopwords(removed_punct)
lemma_words =  topic_extraction.pos_lemmatization(filtered_words)
print(topic_extraction.extract_topic(lemma_words,topic_extraction.topic_length,topic_extraction.num_topic))