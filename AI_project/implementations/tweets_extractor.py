import tweepy
import pandas as pd
import spacy
import torch
import geopy
import folium
from geopy.exc import GeocoderTimedOut
from config import *

nlp = spacy.load('en_core_web_sm')



#put markers on the map.
# data include the locations coordinates to be marked 
#marker_color: the marker color
def put_markers(map, data,marker_color):
    geo_locator = geopy.geocoders.Nominatim(user_agent="LearnPython")
    for (name, location) in data:
        if location:
            try:
                location = geo_locator.geocode(location)
            #except GeocoderTimedOut:
            except Exception as e:
                continue
            if location:
                folium.Marker([location.latitude, location.longitude], popup=name,icon=folium.Icon(color=marker_color)).add_to(map)


# make 3 heat map layers.
#opposed_llist : includes oppsed tweet lines in the file tweets.tsv
#supporter_llist : includes support tweet lines in the file tweets.tsv
#neutral_llist : includes neutral tweet lines in the file tweets.tsv

                
def make_heat_map(opposed_llist, supporter_llist , neutral_llist ):
    # reader = pd.read_csv('output1.tsv')
    df = pd.read_csv('tweets.tsv', sep='\t')
    opposed_rows = df.iloc[opposed_llist, [4, 5]]
    supporter_rows = df.iloc[supporter_llist, [4, 5]]
    neutral_rows = df.iloc[neutral_llist, [4, 5]]
    records1 = opposed_rows.to_records(index=False)
    result1 = list(records1)
    records2 = supporter_rows.to_records(index=False)
    result2 = list(records2)
    records3 = neutral_rows.to_records(index=False)
    result3 = list(records3)
    return result1,result2,result3



# make map that show all the stances.
#opposed_llist : includes oppsed tweet lines in the file tweets.tsv to be marked with red color
#supporter_llist : includes support tweet lines in the file tweets.tsv to be marked with green color
#neutral_llist : includes neutral tweet lines in the file tweets.tsv to be marked with black color

def make_gmap(opposed_llist, supporter_llist , neutral_llist ):
        df =pd.read_csv('tweets.tsv', sep='\t')
        opposed_rows = df.iloc[opposed_llist, [2,3]]
        supporter_rows = df.iloc[supporter_llist, [2,3]]
        neutral_rows = df.iloc[neutral_llist, [2,3]]
        records1 = opposed_rows.to_records(index=False)
        result1 = list(records1)
        records2 = supporter_rows.to_records(index=False)
        result2 = list(records2)
        records3 = neutral_rows.to_records(index=False)
        result3 = list(records3)
        map = folium.Map(location=[0, 0], zoom_start=2)
        put_markers(map, result1,'red')
        put_markers(map, result2,'green')
        put_markers(map, result3,'black')
        map.save("stance_map.html")

        
#remove tokens from string that are not alphabetic such as smiley        
def cleaner(string):
    # Generate list of tokens
    doc = nlp(string)
    lemmas = [token.lemma_ for token in doc]
    # Remove tokens that are not alphabetic
    a_lemmas = [lemma for lemma in lemmas if lemma.isalpha()
                or lemma == '-PRON-']
    # Print string after text cleaning
    return ' '.join(a_lemmas)


#activate twitter api 
def Twitter_API():
    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    # authentication of access token and secret
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api



# get tweets according to the hashtags_list , for each tweet save the text, screen name of the user and the location of the user. save  the tweets data in #tweets_tmp.tsv file 
def get_tweets():
    api = Twitter_API()
    list_tweets_all_hashtags = []
    hashtags_list = ["#abortion" ,"#abortions","#prolife","#prochoice","#abortionismurder" ,"#abortionisnotmurder",
                     "#abortionisahumanright","#abortionrights","#prolifegeneration""#mybodymychoice","#abortionishealthcare" ,
                     "#abortionban","#abortionpositive","#antiabortion","#abortionisevil","#plannedparenthood",
                     "#abortionisawomansright","#abortionisnormal"]


    for hashtag in hashtags_list:
        list_by_tag1 = tweepy.Cursor(api.search, q=hashtag+" -filter:retweets" , tweet_mode='extended', lang='en', bounding_box=[-105.301758,39.964069 ,-105.178505,40.09455]).items(1000)
        list_tweets_all_hashtags.extend(list_by_tag1)

    output = []
    for tweet in list_tweets_all_hashtags:
        if hasattr(tweet, 'user') and hasattr(tweet.user, 'screen_name') and hasattr(tweet.user, 'location'):
            if tweet.user.location:
                text = tweet._json["full_text"]
                text = cleaner(text)
                line = {'text': text, 'screen_name' : tweet.user.screen_name,'location':tweet.user.location}
                output.append(line)

    df = pd.DataFrame(output)
    # dropping duplicate tweets
    df.drop_duplicates(keep="first",inplace=True)
    df.to_csv("tweets_tmp.tsv", header=True,index=True, sep='\t', mode='a')
    return output


# get the place name and return the coordinates of it.
def get_lat_long(place):
    geolocator = geopy.geocoders.Nominatim(user_agent="LearnPython")
    location = geolocator.geocode(place)
    print((location.latitude, location.longitude))


if __name__ == "__main__":
    get_tweets()
