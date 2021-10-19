import tweepy
import pandas as pd
import geopy
import spacy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from config import *


#activate twitter API
def Twitter_API():
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    # authentication of access token and secret
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api



#extract the local id numbers saved in input file
def get_local_ids(file):
    f = open(file, "r")
    lines = f.readlines()
    result = []
    for line in lines:
        id = int(line.split()[0])
        result.append(id)
    f.close()
    return  result


#extract the tweet id numbers of specifid lines of the file
#file : file to read
#lines_to_read: the numer of the lines to read
def get_tweets_id(file,lines_to_read):
    f = open(file)
    dict = {}
    for i, line in enumerate(f):
        if(i==0):
            continue
        current_id = int(line.split()[0])
        tweet_id = int(line.split()[1])

        if current_id in lines_to_read:
            dict.update({current_id:tweet_id})
    f.close()
    return dict


#extract the location for each tweet in a given tweets dictionary, and save the result in a file 
#tweets_dict : dictionay of tweets, the key is the local tweet id in a file, and tweet id in the twitter is the value. 
#file_name : the output file name 

def extarct_tweets_data(tweets_dict,file_name):
    api = Twitter_API()
    output = []
    geolocator = geopy.geocoders.Nominatim(user_agent="LearnPython")
    for local_id, tweet_id in tweets_dict.items():
        try:
            status = api.get_status(tweet_id)
        except tweepy.TweepError:
            continue

        if status.user.location != '':
            try:
              location = geolocator.geocode(status.user.location)
            except Exception:
                continue
                #place = status.user.location
            if location == None :
                continue
            line = {'ID' :local_id, 'tweet id':tweet_id, 'LAT': location.latitude , 'LON':location.longitude}
            output.append(line)
    df = pd.DataFrame(output)
    df.to_csv(file_name, header=True, index=False, sep='\t', mode='a')
    return



#merge two files
#file1 : the first file 
#file2 : the second file to merge with.

def combine_files(file1,file2):
    # reading csv files
    data1 = pd.read_csv("data-all-annotations/legalization_of_abortion_test_set.txt")
    data2 = pd.read_csv(file2)

    # using merge function by setting how='left'
    output2 = pd.merge(data1, data2,
                       on='LOAN_NO',
                       how='inner')
    # displaying result
    #print(output2)
    
    
#convert the file content to dictionary, for each file line converts it to dictionary element
#such that the key is the value in the first column and the value is the second column of the line.

def file_to_dictionary(file_path):
    dict = {}
    file = open(file_path)
    first_line = True
    for line in file:
        if first_line:
            first_line= False
            continue
        key = line.split()[0]
        value = int(line.split()[1])
        dict[key] = value
    return dict


if __name__ == "__main__":

    ## Extracting user location for legalization_of_abortion_test_set

    local_ids = get_local_ids("../data-all-annotations/legalization_of_abortion_test_set.txt")
    tweets_id = get_tweets_id("../data-all-annotations/testdata-taskA-ids.txt",local_ids)
    extarct_tweets_data(tweets_id,"legalization_of_abortion_test_set_location25-8.csv")

    data1 = pd.read_csv('../data-all-annotations/legalization_of_abortion_test_set.txt', sep='\t')
    data1.columns = ['ID', 'Target', 'Text', 'Stance', 'Opinion towards', 'Sentiment']

    data2 = pd.read_csv("legalization_of_abortion_test_set_location25-8.csv", sep='\t')
    output2 = pd.merge(data1, data2,
                       on='ID',
                       how='inner')
    output2 = output2.drop(['tweet id'], axis=1)
    output2.to_csv("legalization_of_abortion_test_set_full25-8.txt", index=False, header=False, sep='\t')


    ## Extracting user location for Training all annotation
    
    tweets_id = file_to_dictionary("../data-all-annotations/trainingdata-ids.txt")
    extarct_tweets_data(tweets_id, "trainingdata-ids-place25-8.csv")

    data1 = pd.read_csv("../data-all-annotations/trainingdata-all-annotations.txt", sep='\t')
    data2 = pd.read_csv("trainingdata-ids-place25-8.csv", sep='\t')

    output2 = pd.merge(data1, data2,
                       on='ID',
                       how='inner')
    output2 = output2.drop(['tweet id'], axis=1)
    output2.to_csv("trainingdata-ids-full-25-8-FINAL.txt", index=False, header=False, sep='\t')
