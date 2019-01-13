import re
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import math
from collections import Counter
from nltk.corpus import wordnet
class topic_extraction:
    
    def __init__(self,url,num_topic,topic_length):
        self.url = url
        self.num_topic = num_topic
        self.topic_length = topic_length 

    def get_url_response(url):
        """
        sends the HTTP/1.1 request to the server.
        returns a response that can be used to get the Page Source, response status code, etc.

        -----------------
        Format Type : requests.models.Response
        example: 
        get_url_response(<url>)
        Returns : <Response [<status code>]>
        """
        http_status_code = {204: 'No Content!',400: 'Bad Request!',401: 'Unauthorized!',403: 'Forbidden!',
                            404: 'Not Found!',408: 'Request Timeout!',500: 'Internal Server Error!',
                            503: 'Service is Unavailable!',
                           }
        headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
        try:
            response =  requests.get(url = url,headers = headers, timeout =5)
            if not(str(response.status_code).startswith('2')):
                if response.status_code in http_status_code:
                    raise Exception("ERROR {}: {}".format(response.status_code,http_status_code[response.status_code]))
                else:
                    raise Exception('ERROR {}'.format(response.status_code))
            print('Request passed successfully with the status code {}'.format(response.status_code))
            return response
        except requests.exceptions.RequestException as error:
            print(error)

    def get_page_text(response):
        """
        Takes a response and returns the filtered contents of the web page.
        ----------
        Format Type : list
        """
        try:
            # used "lxml" as parser to parse html;
            soup =  BeautifulSoup(response.content,'lxml')
            # Remove tags such as ["style","script","nav","header","form","a",'table','footer'] 
            # that does not help in identifying the topic of the page
            for script in soup(["style","script","header","nav","a","form",'table','footer']):
                script.extract() 
            # Get meta tag texts
            meta_text = [i.attrs.get('content') for i in soup.find_all('meta')]
            # Get title and h1 text
            title_text = [i.text for i in soup.find_all(['title'])]
            # Get Body Text
            body_text = [i for i in soup.body.stripped_strings]
            page_text = (meta_text + title_text + body_text)
            # Remove if any None value
            page_text = [x for x in page_text if x is not None]
            # filter the page_text if the corresponding line of text has number of words >=3 and
            # has first index has alphabet and not a number/character.
            page_text = [x for x in page_text if len(x.split()) >=3 and (x.split()[0].isalpha())]
            # Lower Case page_text
            page_text = [i.lower() for i in page_text]
            print('parsed page successfully')
            return page_text
        except Exception as e:
            print("Error:{}".format(e))
    
    def stemming(page_text):
        '''
        extracts the root of a word.
        For Example, the word "grows" becomes "grow".
        '''
        # intialised porter stemmer
        stemmer = PorterStemmer()
        words_stem =  [stemmer.stem(word) for word in page_text]
        return ' '.join(words_stem)
    
    def get_wordnet_pos(tag_string):
        """
        This function returns the part of speech tag which in then is used to lemmatization
        J Denotes Adjectives
        V Denotes Verbs
        N Denotes Noun
        R Denotes Adverbs
        """
        if tag_string.startswith('J'):
            return wordnet.ADJ
        elif tag_string.startswith('V'):
            return wordnet.VERB
        elif tag_string.startswith('N'):
            return wordnet.NOUN
        elif tag_string.startswith('R'):
            return wordnet.ADV
        else:
            return 'n'

    def remove_punctuation(page_text):
        """
        Removes the puntuation from the page text using regex substitution method.
        Input : list of strings.
        output: string 
        ---------
        For example, for the "xyz's abc$*&@ *#", it will return "xyz's abc". 
        It will not remove "'" as it useful.
        """
        removed_punct = []
        for sentence in page_text:
            sentence = re.sub(r"[^a-zA-Z0-9\-'\s]", ' ', sentence)
            removed_punct.append(re.sub(' +',' ',sentence))
        print("Removed Puntuation")
        return removed_punct

    def remove_stopwords(sentence):
        """
        returns the list of words that does not have stop words.
        ------------
        input: str
        output : list
        """
        filtered_words = []
        stop_words = set(stopwords.words('english'))
        tokenized_sentence =  [word_tokenize(sent) for sent in sentence] 
        
        for sent in tokenized_sentence:
            temp = []
            for word in sent:
                if word not in stop_words:
                    temp.append(word)
            filtered_words.append(temp)
        print('Removed Stopwords')
        return filtered_words

    def pos_lemmatization(filtered_words):
        """
        Returns Lemmatized list of words.
        --------------
        input: list
        output: list
        """
        lemma_words = []
        lemmatizer = WordNetLemmatizer() # initialise WordNetLemmatizer
        for sent in filtered_words:
            temp=[]
            for words in sent:
                pos_ = pos_tag(word_tokenize(words)) # word tokenizer
                for word in pos_:
                    if str(word[1]).startswith(('N','J','V','R')) :
                        temp.append(lemmatizer.lemmatize(word[0],topic_extraction.get_wordnet_pos(word[1])))
            lemma_words.append(temp)
        print("Lemmatized Successfully")
        return lemma_words

    def extract_topic(lemma_words,topic_length=3,num_topic=5):
        """
        Returns the relevant topics for the document by finding most frequently occuring bag of tokens.
        """
        topic_list=[]
        for sentence in lemma_words:
            if(len(sentence)>=topic_length):
                for i in range(len(sentence)-(topic_length-1)):
                    topic_list.append(tuple(sentence[i:i+topic_length]))
        topic_dict =  Counter(topic_list)            
        try:
            if max(topic_dict.values()) >3: #if any topic frequency has more than 3, then we do not need topics which has lowest frequency
                topic_dict = Counter({k:v for k,v in topic_dict.items() if v>1})

        except:
            pass
        if num_topic <= len(topic_dict): # if the number of topic needed is smaller than total topics
            print('Topic extraction performed successfully')
            print("---------------------------------------------------------------------------------")
            print("Revelant topics for the given url are:")
            return [','.join(list(i[0])) for i in topic_dict.most_common(num_topic)] #result
        else:
            raise ValueError("please provide number of topics less than {}".format(len(topic_dict)))