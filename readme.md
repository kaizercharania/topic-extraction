******************************************************************************************************************************
******************************************************************************************************************************


### This module is used to extract topics relevant to the web page that you want to know about.
The module uses:<br />
<br />
--> user-agent library to make server understand that a user is accessing the webpage and not the code<br />
--> Requests library to send a HTTP/1.1 get request to the server.<br />
--> BeautifulSoup library to parse the content of the page source<br />
--> NLTK library to perform Tokenizing, Lemmatizing and various Natural Language Processing techniques<br />
<br />
Before running the module please install the libraries mentioned in "requirements.txt" file<br />
<br />
To get the topics relevant to the webpage that you want to know, perform the following steps:<br />
<br />
1.) Unzip the module<br />
2.) copy-paste "requirements.txt" into the terminal<br />
3.) run the following command "python main.py"<br />
4.) Enter the URL you want to know for<br />
5.) Enter the number of topics you want to see<br />
6.) Enter the length of topic you want to see. For example, if you want to look for 3 word topic, enter 3<br />
7.) And wait for the results<br />

The result will show you what the page is about.<br />
