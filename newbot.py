#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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

import os
import scrapy
from scrapy.crawler import Crawler, CrawlerProcess, CrawlerRunner
from scrapper import webSpider
from twisted.internet import reactor
#from telegrambot import telegrambot
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "1163712269:AAFCz2DxQehxtS3s3yE2gIjGJ6xfWSIMd00"
#PORT = int(os.environ.get('PORT', '8443'))
#APPNAME = "https://whythebot.herokuapp.com/"

greetings = ['Hey', 'Hello', 'Hi', 'It\'s great to see you', 'Nice to see you', 'Good to see you']
bye = ['Bye', 'Bye-Bye', 'Goodbye', 'Have a good day','Stop']
thank_you = ['Thanks', 'Thank you', 'Thanks a bunch', 'Thanks a lot.', 'Thank you very much', 'Thanks so much', 'Thank you so much']
thank_response = ['You\'re welcome.' , 'No problem.', 'No worries.', ' My pleasure.' , 'It was the least I could do.', 'Glad to help.']

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi there! I am your friendly bot. How can I help? \nType Bye to Exit.!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# pre-processing the raw text:

#sc=scrape()
sent_tokens = []
word_tokens = []

def read_corpus():
    # this is where the corpus is read and sentence applied.
    f = open("content.txt",'r',errors = 'ignore', encoding = 'utf-8')
    paragraph = f.read()
    #nltk.download('punkt')   # for first-time use only. Punkt is a Sentence Tokenizer
    #nltk.download('wordnet')    # for first-time use only. WordNet is a large lexical database of English.
    global sent_tokens 
    global word_tokens
    sent_tokens = nltk.sent_tokenize(paragraph)
    word_tokens = nltk.word_tokenize(paragraph)
    #return sent_tokens
####################################

# Lemmitization
lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):    
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
    return LemTokens(nltk.word_tokenize(text.lower().translate(removepunct())))
# lemmitization end

def get_tfidf(msg):
    print("looking for ",msg)
    sent_tokens.append(msg)   # Appending the Question user ask to sent_tokens to find the Tf-Idf and cosine_similarity between User query and the content.
    print("sent tokens = ",sent_tokens)
    TfidfVec = TfidfVectorizer(tokenizer = Normalize, stop_words='english')    #tokenizer ask about Pre-processing parameter and it will consume the Normalize() function and it will also remove StopWords
    print ("hi\n")
    #print(f"tfidfvec ={TfidfVec}")
    tfidf = TfidfVec.fit_transform(sent_tokens)
    #print ("tfidf = ",tfidf)
    vals = cosine_similarity(tfidf[-1], tfidf)     # It will do cosine_similarity between last vectors and all the vectors because last vector contain the User query
    #if (len(vals) == 1):
    #    req_tfidf = 0
    #else:        
    global idx
    idx = vals.argsort()[0][-2]     # argsort() will sort the tf_idf in ascending order. [-2] means second last index i.e. index of second highest value after sorting the cosine_similarity. Index of last element is not taken as query is added at end and it will have the cosine_similarity with itself.
    flat = vals.flatten()    # [[0,...,0.89,1]] -> [0,...,0.89,1] this will make a single list of vals which had list inside a list.
    flat.sort()
    req_tfidf = flat[-2]  # this contains tfid value of second highest cosine_similarity
    print("req tfidf = ",req_tfidf)
    return req_tfidf

def learntresponse(msg, track):
    print("i am here as well \n")
    robo_response = ''    
    tfidf_val = get_tfidf(msg)
    print("what about here ? \n")
    if (tfidf_val == 0):
        #track = 0
        if track == 0:
            robot_response = []
            learn = 0
            robo_response = robo_response + "I'm learning, please hang on!"
            #track += 1
            robot_response = [learn,robo_response]
            return robot_response
            # invoke scrapy here        
            #read_corpus(sc.scrape_user_response(msg))
            # invoke content parsing + lemmitization on new data
            #tfidf_val = get_tfidf(msg)
    #elif (tfidf_val == 0 and track == 0):    # 0 means there is no similarity between the question and answer
        else: #(tfidf_val == 0 and track == 1):    # 0 means there is no similarity between the question and answer
        #robo_response = robo_response + "I'm learning, please hang on!"
        #track += 1
        #print("track = ",track)
        # invoke scrapy here        
        #read_corpus(sc.scrape_user_response(msg))
        # invoke content parsing + lemmitization on new data
        #tfidf_val = get_tfidf(msg)
        #if(tfidf_val == 0 and track == 1):
            learn = 1
            robo_response = '' + "I am sorry! I didn't understand. Please rephrase your query."
            robot_response = [learn,robo_response]
            return robot_response
    
    else:
        learn = 2
        robo_response = robo_response + sent_tokens[idx]    # return the sentences at index -2 as answer
        robot_response = [learn,robo_response]
        return robot_response

def invokeScrapy(user_msg):
    QUERY = user_msg
    #crawler = Crawler(webSpider)
    #process = CrawlerProcess()
    runner = CrawlerRunner()
    r = runner.crawl(webSpider, QUERY)
    r.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished

def bot_init(update, context):
    flag=True
    #while(flag==True):
    user_response = update.message.text
    if(user_response not in bye):
        if(user_response == '/start'):
            bot_resp = "Hi! There. I am your friendly bot. How can I help? \nType Bye to Exit."
            #context.bot.send_message(chat_id=update.effective_chat.id, text=bot_resp)
            update.message.reply_text(bot_resp)
            #return bot_resp
        elif(user_response in thank_you):
            bot_resp = random.choice(thank_response)
            #context.bot.send_message(chat_id=update.effective_chat.id, text=bot_resp)
            update.message.reply_text(bot_resp)
            #return bot_resp
        elif(user_response in greetings):
            bot_resp = random.choice(greetings) + ", What info are you looking for?"
            #context.bot.send_message(chat_id=update.effective_chat.id, text=bot_resp)
            update.message.reply_text(bot_resp)
            #return bot_resp
        else:
            user_response = user_response.lower()
            print("I am here\n")
            robot_resp = learntresponse(user_response,0)
            if robot_resp[0] == 0:
                print("and here \n")
                update.message.reply_text(robot_resp[1])
                # invoke scrapy
                invokeScrapy(user_response)        
                #read_corpus(QUERY.replace(" ","")+".txt")
                read_corpus()
                #read_corpus(sc.scrape_user_response(user_response))
                bot_resp = learntresponse(user_response,1)
            elif robot_resp[0] == 1:
                sent_tokens.remove(user_response)   # remove user question from sent_token that we added in sent_token in response() to find the Tf-Idf and cosine_similarity
                update.message.reply_text(robot_resp[1])
            else:
                sent_tokens.remove(user_response)
                update.message.reply_text(robot_resp[1])
            #    return bot_resp
    else:
        flag = False
        bot_resp = random.choice(bye)
        update.message.reply_text(bot_resp)
        #context.bot.send_message(chat_id=update.effective_chat.id, text=bot_resp)
        #return bot_resp




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    nltk.download('punkt')   # for first-time use only. Punkt is a Sentence Tokenizer
    nltk.download('wordnet')    # for first-time use only. WordNet is a large lexical database of English.
    read_corpus()
    up = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = up.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("start", bot_init('/start')))
    # dp.add_handler(CommandHandler("help", help))
    
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, bot_init))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    up.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    up.idle()


if __name__ == '__main__':
    main()