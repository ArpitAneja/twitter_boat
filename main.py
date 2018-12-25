# import the api of twitter
import tweepy

# python library for processing textual data
from textblob import TextBlob

# python library for sub method used to replace url string with ''
import re

# python library for predefined stop words
import nltk
from nltk.corpus import stopwords

# generated from apps.twitter.com
from credentials import api_key,api_secret,access_token,access_token_secret

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token,access_token_secret)

# here api stores the twitter API with authentication details we provided
api=tweepy.API(auth)

user_tweet = []

# getsearch is a function which take a hashtag as argument and returns tweets as object of status class
def getsearch(query):
   tweets = api.search(q=query,count = 20)
   for tweet in tweets:
       print(tweet)

# getinfo functions display name and no of followers who tweeted the tweet containing word defined by user
def getinfo(query):
    tweets = api.search(q=query, count=20)
    for tweet in tweets:
        print("Name: " + tweet.user.screen_name+"   Followers: "+str(tweet.user.followers_count))

# this function analyse the tweet is negative, neutral or positive
def senti_analysis(hashtag):
    negative = 0
    neutral = 0
    positive = 0
    count = 0
    tweets = api.search(q=hashtag, count=20)
    for tweet in tweets:
        count += 1
        analyse = TextBlob(tweet.text)
        if analyse.sentiment.polarity < 0:
            negative += 1
        elif analyse.sentiment.polarity == 0:
            neutral += 1
        elif analyse.sentiment.polarity > 0:
            positive += 1
    print("No of tweets considered for %s are: %d\nsentiments for this tweet are:\npositive:%d\nneutral:%d\nnegative:%d"%(hashtag,count,positive,neutral,negative))


def locations(hashtag):
    tweets = api.search(q=hashtag, count=200)
    location = {}
    time_zone ={}
    language = {}
    for tweet in tweets:
        # tracking locations and their frequencies
        loc = tweet.user.location
        if loc in location.keys():
            location[loc] += 1
        elif loc != '':
            location[loc] = 1

        # tracking time zones and their frequencies
        time = tweet.user.time_zone
        if time in time_zone.keys():
            time_zone[time] += 1
        elif time_zone != '':
            time_zone[time] = 1

        # tracking languages and their frequencies
        lang = tweet.user.lang
        if lang in language.keys():
            language[lang] += 1
        elif lang != '':
            language[lang] = 1

    # standardizing  the result so that it shows items with maximum frequencies
    top_location = sorted(location, key=location.get, reverse=True)
    top_time_zone = sorted(time_zone, key=time_zone.get, reverse=True)
    top_language = sorted(language, key=language.get, reverse=True)



    # displaying top 5 maximum occurred locations
    i = 0 #serial number
    print("most people "+hashtag+" tweeted this belong to locations:")
    for r in top_location[:5]:
        i += 1
        print("%d. %s    count: %d"%(i, r, location[r]))

    # displaying top 5 maximum occurred time zone
    i = 0  # serial number
    print("time zone of people who tweeted " + hashtag + " are:")
    for r in top_time_zone[:5]:
        i += 1
        print("%d. %s    count: %d"%(i, r, time_zone[r]))

    # displaying top 5 maximum occurred time zone
    i = 0  # serial number
    print("language of people who tweeted the tweet:")
    for r in top_language[:5]:
        i += 1
        print(i, r, language[r])

def s_user():
    name = input("enter whose tweet you want to compare:\n 1.Narendra Modi\n 2.Donald Trump\n ")

    if name == '1':
        name = 'narendramodi'
        ref_string = ['America', 'US', 'USA', 'United States of America']
    elif name == '2':
        name = 'realDonaldTrump'
        ref_string = ['India', 'india']
    counter = 0

    timeline = api.user_timeline(screen_name=name,count=200,tweet_mode="extended")

    for tweet in timeline:
        tweet = re.sub(r"http\S+", "", tweet.full_text)  # removing the url's from tweets
        user_tweet.append(tweet)

    for tweet in user_tweet:
        print(tweet)

    for i in user_tweet:
        parser = i.split(" ")
        for word in parser:
            if word in ref_string:
                    counter += 1
    print(name + " tweeted " + ref_string[0] + ":"+str(counter)+" times")


def top_use():
    top_word = {}
    user_tweet = []
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    counter = 0
    timeline = api.user_timeline(screen_name='narendramodi', count=10, tweet_mode="extended")

    for tweet in timeline:
        tweet = re.sub(r"http\S+", "", tweet.full_text)
        user_tweet.append(tweet)

    for i in user_tweet:
        parser = i.split(" ")
        for word in parser:
            if word not in stop_words and word not in ' ':
                counter += 1
                top_word[word] =counter

    # storing words in descending order according to frequency
    des_top_word  = sorted(top_word, key=top_word.get, reverse=True)
    i=0
    print("the top ten most used words are:")
    for word in des_top_word[:10]:
        i += 1
        print(i,word)

def update_status(status):
    api.update_status(status)
    print("status uploaded successfully")


def main():
    # showing a menu with options till user enters exit
    show_menu = True
    while show_menu:
        print("1.Retrieve tweets \n"
              "2.Count number of followers\n"
              "3.Determine the sentiments\n"
              "4.Determine location, time zone and language\n"
              "5.Compare tweets\n"
              "6.Top usage\n"
              "7.Update your status\n"
              "8.Exit")
        choice = int(input("enter your choice"))
        # Retrieve tweets
        if choice == 1:
            query = input("enter word(without #) you want to retrieve tweets of:")
            # added '#' to query to make it an hashtag to limit the search for defined word
            hashtag = "#" + query
            getsearch(hashtag)
        #  Count number of followers
        elif choice == 2:
            query = input("enter hashtag(without #) you want to count followers of:")
            hashtag = "#" + query
            getinfo(hashtag)
        # Determine the sentiments
        elif choice == 3:
            query = input("enter the word you want to conduct tweets sentiment analysis on:")
            hashtag = "#" + query
            senti_analysis(hashtag)
        # Determine location, time zone and language
        elif choice == 4:
            query = input("enter the word for tweets you want to get time zone,location,language of:")
            hashtag = "#" + query
            locations(hashtag)
        # Compare tweets
        elif choice == 5:
           s_user()
        # Top usage
        elif choice == 6:
            top_use()
        # Update your status
        elif choice == 7:
            status = input("enter status:")
            update_status(status)
        # Exit
        if choice == 8:
            show_menu = False

# calling the main function
main()