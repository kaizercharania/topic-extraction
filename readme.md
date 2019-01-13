This module is used to extract topics relevant to the web page you want to know. 
The module uses:
--> user-agent library to make server understand that a user is accessing the webpage and not the code
--> Requests library to send a HTTP/1.1 get request to the server.
--> BeautifulSoup library to parse the content of the page source
--> NLTK library to perform Tokenizing, Lemmatizing and various Natural Language Processing techniques

Before running the module please install the libraries mentioned in "requirements.txt" file

To get the topics relevant to the webpage that you want to know, perform the following steps:

1.) Unzip the module
2.) copy-paste "requirements.txt" into the terminal
3.) run the following command "python main.py"
4.) Enter the URL you want to know for
5.) Enter the number of topics you want to see
6.) Enter the length of topic you want to see. For example, if you want to look for 3 word topic, enter 3
7.) And wait for the results

The result will show you what the page is about.
