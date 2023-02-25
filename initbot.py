import random
import nltk
import numpy as np
import string
import warnings
warnings.filterwarnings("ignore")
# From scikit learn library, import the TFidf vectorizer to convert a collection of raw documents to a matrix of TF-IDF features.
from sklearn.feature_extraction.text import TfidfVectorizer
# Also, import cosine similarity module from scikit learn library
from sklearn.metrics.pairwise import cosine_similarity

from scrape import scrape
from telegrambot import telegrambot

greetings = ['Hey', 'Hello', 'Hi', 'It\'s great to see you', 'Nice to see you', 'Good to see you']
bye = ['Bye', 'Bye-Bye', 'Goodbye', 'Have a good day','Stop']
thank_you = ['Thanks', 'Thank you', 'Thanks a bunch', 'Thanks a lot.', 'Thank you very much', 'Thanks so much', 'Thank you so much']
thank_response = ['You\'re welcome.' , 'No problem.', 'No worries.', ' My pleasure.' , 'It was the least I could do.', 'Glad to help.']
# Example of how bot match the keyword from Greetings and reply accordingly

sc=scrape()
#sent_tokens = []

def read_corpus(filename):
    # this is where the corpus is read and sentence applied.
    f = open(filename,'r',errors = 'ignore', encoding = 'utf-8')
    paragraph = f.read()
    nltk.download('punkt')   # for first-time use only. Punkt is a Sentence Tokenizer
    nltk.download('wordnet')    # for first-time use only. WordNet is a large lexical database of English.
    sent_tokens = nltk.sent_tokenize(paragraph)
    word_tokens = nltk.word_tokenize(paragraph)
    return sent_tokens, word_tokens;
####################################

# pre-processing the raw text:
# Lemmitization

def LemTokens(tokens):
    lemmer = nltk.stem.WordNetLemmatizer()
    return [lemmer.lemmatize(token) for token in tokens]    # iterate through every token and lemmatize it
# string.punctuation has all the punctuations
# ord(punct) convert punctuation to its ASCII value
# dict contains {ASCII: None} for punctuation mark
def removepunct():
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return remove_punct_dict
# This will return the word to LemTokens after Word tokenize, lowering its case and removing punctuation mark
# translate will find punctuation mark in remove_punct_dict and if found replace it with None
def Normalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(removepunct)))
# lemmitization end



def bot_init(user_msg):
    flag=True
    while(flag==True):
        user_response = user_msg
        if(user_response not in bye):
            if(user_response == '/start'):
                bot_resp = """Hi! There. I am your friendly bot. How can I help? \nType Bye to Exit.""" 
                return bot_resp
            elif(user_response in thank_you):
                bot_resp = random.choice(thank_response)
                return bot_resp
            elif(user_response in greetings):
                bot_resp = random.choice(greetings) + ", What info are you looking for?"
                return bot_resp
            else:
                user_response = user_response.lower()
                bot_resp = response(user_response)
                sent_tokens.remove(user_response)   # remove user question from sent_token that we added in sent_token in response() to find the Tf-Idf and cosine_similarity
                return bot_resp
        else:
            flag = False
            bot_resp = random.choice(bye)
            return bot_resp

        # 1. set counter=0 here, in the first attempt if tfidf returns 0
        # 2. send response "i'm learning, hang on"
        # incrment counter to 1
        # invoke scrapy; hopefully now it'll have content to respond from
        # check if tfidf==0 and counter==1
        # respond user to rephrase and set counter = 0
        # loop initiates all over again ie: call response() again when user rephrases and posts
        

def response(user_response):
    robo_response = ''
    track = 0
    tfidf_val = get_tfidf(user_response)
    if(tfidf_val == 0 and track == 0):    # 0 means there is no similarity between the question and answer
        robo_response = robo_response + "I'm learning, please hang on!"
        track = track + 1
        # invoke scrapy here        
        sent_tokens = read_corpus(sc.scrape_user_response(user_response))
        # invoke content parsing + lemmitization on new data
        tfidf_val = get_tfidf(user_response)
        if(tfidf_val == 0 and track == 1):
            robo_response = '' + "I am sorry! I don't understand you. Please rephrase your query."
            track = 0
            return robo_response
    
    else:
        robo_response = robo_response + sent_tokens[idx]    # return the sentences at index -2 as answer        
        return robo_response


def get_tfidf(user_response):
        
    sent_tokens.append(user_response)   # Appending the Question user ask to sent_tokens to find the Tf-Idf and cosine_similarity between User query and the content.
    TfidfVec = TfidfVectorizer(tokenizer = Normalize, stop_words='english')    #tokenizer ask about Pre-processing parameter and it will consume the Normalize() function and it will also remove StopWords
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)     # It will do cosine_similarity between last vectors and all the vectors because last vector contain the User query
    idx = vals.argsort()[0][-2]     # argsort() will sort the tf_idf in ascending order. [-2] means second last index i.e. index of second highest value after sorting the cosine_similarity. Index of last element is not taken as query is added at end and it will have the cosine_similarity with itself.
    flat = vals.flatten()    # [[0,...,0.89,1]] -> [0,...,0.89,1] this will make a single list of vals which had list inside a list.
    flat.sort()
    req_tfidf = flat[-2]  # this contains tfid value of second highest cosine_similarity
    return req_tfidf
    
tbot = telegrambot()
update_id = None
def make_reply(msg):     # user input will go here
  
    if msg is not None:
        reply = bot_init(msg)     # user input will start processing to bot_initialize function
    return reply
       
while True:
    print("...")    
    updates = tbot.get_updates(offset=update_id)
    updates = updates['result']
    print(updates)
    if updates:
        for item in updates:
            update_id = item["update_id"]
            print(update_id)
            try:
                message = item["message"]["text"]
                print(message)
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            print(from_)

reply = make_reply(message)
tbot.send_message(reply,from_)    
