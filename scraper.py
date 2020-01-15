import json
import csv
import tweepy
import re
import config
import os
import wget

def to_textfile():
    csv_file = '%s.csv' % (fname)
    text_file = open("twitter.txt",'a+')
    with open(csv_file, 'r', encoding='utf-8') as csvfile:

        # get number of columns
        for line in csvfile.readlines():
            array = line.split(',')
            first_item = array[0]

        num_columns = len(array)
        csvfile.seek(0)

        reader = csv.reader(csvfile, delimiter=',')
        included_cols = [2]

        for row in reader:
                if row:
                    text_file.write(row[1]+"\n")

def search_for_hashtags(consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase):

    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)

    #get the name of the spreadsheet we will write to


    #open the spreadsheet we will write to
    with open('%s.csv' % (fname), 'w', encoding = "utf-8") as file:

        w = csv.writer(file)

        #write header row to spreadsheet
        #w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])
        media_files = set()
        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        all_tweets =  tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets', lang="en", tweet_mode='extended').items(300)
        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in all_tweets:
            w.writerow([tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name, [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])
            media = tweet.entities.get('media', [])
            if(len(media) > 0):
                media_files.add(media[0]['media_url'])
        new_path= os.getcwd()+"\pictures"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        os.chdir(new_path)
        for media_file in media_files:
            wget.download(media_file)
        os.chdir('..')

hashtag_phrase = input('Hashtag Phrase: ')
fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))
search_for_hashtags(config.consumer_key,config.consumer_secret,config.access_token,config.access_token_secret,hashtag_phrase)
to_textfile()
