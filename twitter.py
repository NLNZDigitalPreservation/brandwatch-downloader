import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from hashlib import md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s
from twarc import Twarc
import emoji
import re, sys, configparser
from datetime import datetime
import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np

config = configparser.ConfigParser()
config.read('.env')


    
class Twitter:
    def __init__(self, isHash=True):    
        try:
            config['credentials']
        except:
            print('Please save your credentials into .env file')
        if 'credentials' in config:
            self.consumer_key = config['credentials']['consumer_key']
            self.consumer_secret = config['credentials']['consumer_secret']
            self.access_token = config['credentials']['access_token']
            self.access_token_secret = config['credentials']['access_token_secret']
            self.t = Twarc(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)
            self.user_id_dict = {}
            self.user_name_dict = {}
            self.user_screen_name_dict = {}
            self.isHash = isHash
    
    def getUserDetails(self, value, dict_type='id'):
        if dict_type == 'id':
            if value not in self.user_id_dict.keys():
                self.user_id_dict[value] = self.getHash(value)                
            value_hash = self.user_id_dict[value]
        elif dict_type == 'name':
            if value not in self.user_name_dict.keys():
                self.user_name_dict[value] = self.getHash(value)
            value_hash = self.user_name_dict[value]
        elif dict_type == 'screenname':
            if value not in self.user_screen_name_dict.keys():
                self.user_screen_name_dict[value] = self.getHash(value)
            value_hash = self.user_screen_name_dict[value]
        return value_hash

    def getHash(self, value, algo='sha1'):
        if algo == 'md5':
            hex_dig = md5(value.encode('utf-8')).hexdigest()
        elif algo == 'sha1':
            hex_dig = sha1(value.encode('utf-8')).hexdigest()
        elif algo == 'sha224':
            hex_dig = sha224(value.encode('utf-8')).hexdigest()
        elif algo == 'sha256':
            hex_dig = sha256(value.encode('utf-8')).hexdigest()
        elif algo == 'sha384':
            hex_dig = sha384(value.encode('utf-8')).hexdigest()
        elif algo == 'sha512':
            hex_dig = sha512(value.encode('utf-8')).hexdigest()
        elif algo == 'blake2b':
            hex_dig = blake2b(value.encode('utf-8')).hexdigest()
        elif algo == 'blake2s':
            hex_dig = blake2s(value.encode('utf-8')).hexdigest()
        return hex_dig
    
    def getItemsByIds(self, ids):
        items = self.t.hydrate(ids)
        results = []
        for item in items:
            if self.isHash:
                user_id = self.getUserDetails(item['user']['id_str'], 'id')
                user_name = self.getUserDetails(item['user']['name'], 'name')
                user_screen_name = self.getUserDetails(item['user']['screen_name'], 'screenname')
                tweet_url = self.getHash("https://twitter.com/" + user_screen_name + "/status/" + str(item['id']))
            else:
                user_id = item['user']['id_str']
                user_name = item['user']['name']
                user_screen_name = item['user']['screen_name']
                tweet_url = "https://twitter.com/" + user_screen_name + "/status/" + str(item['id'])
        
            if 'full_text' in item:
                tweet_text = emoji.demojize(item['full_text'].replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\u2066', '').replace('\u2069', '').replace('|', '-'))
            elif 'text' in item:
                tweet_text = emoji.demojize(item['text'].replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\u2066', '').replace('\u2069', '').replace('|', '-'))
            
            user_desc = emoji.demojize(item['user']['description'].replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\u2066', '').replace('\u2069', '').replace('|', '-'))

            location = item['user']['location'].replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ').replace('\u2066', '').replace('\u2069', '').replace('|', '-')

            source = re.compile(r'<[^>]+>').sub('', item['source'])

            retweeted_user_id = ''
            retweeted_tweet_id = ''
            
            if "retweeted_status" in item and item['retweeted_status'] is not None:
                if self.isHash:
                    retweeted_tweet_id = self.getHash(item["retweeted_status"]['id_str'])
                    retweeted_user_id = self.getUserDetails(item["retweeted_status"]['user']['id_str'], 'id')
                else:
                    retweeted_tweet_id = item["retweeted_status"]['id_str']
                    retweeted_user_id = item["retweeted_status"]['user']['id_str']

            in_reply_to_user_id_str = ''
            if 'in_reply_to_user_id_str' in item and item['in_reply_to_user_id_str'] is not None:
                if self.isHash:
                    in_reply_to_user_id_str = self.getUserDetails(item['in_reply_to_user_id_str'],'id')
                else:
                    in_reply_to_user_id_str = item['in_reply_to_user_id_str']
              
            hashtags = []
            if(item['entities']['hashtags']):
                for hashtag in item['entities']['hashtags']:
                    hashtags.append(hashtag['text'])
            user_mentions = []
            if(item['entities']['user_mentions']):
                for mention in item['entities']['user_mentions']:
                    if self.isHash:
                        user_mentions.append(self.getUserDetails(mention['id_str'], 'id'))
                    else:
                        user_mentions.append(mention['id_str'])
            urls = []
            if(item['entities']['urls']):
                for url in item['entities']['urls']:
                    if "expanded_url" in url:
                        urls.append(url['expanded_url'])
                    elif "url" in url:
                        urls.append(url['url'])

            tweet_date = datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            user_date = datetime.strptime(item['user']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

            results.append({'tweetid':item['id'],'tweet_url':tweet_url,'userid':user_id,'user_display_name':user_name,'user_screen_name':user_screen_name,'user_reported_location':location,'user_profile_description':user_desc,'user_profile_url':item['user']['url'],'follower_count':item['user']['followers_count'],'following_count':item['user']['friends_count'],'account_creation_date':user_date.strftime("%a %b %d %H:%M:%S +0000 %Y"),'account_language':item['user']['lang'],'tweet_language':item['lang'],'tweet_text':tweet_text,'tweet_time':tweet_date.strftime("%a %b %d %H:%M:%S +0000 %Y"),'tweet_client_name':source,'in_reply_to_userid':in_reply_to_user_id_str,'in_reply_to_tweetid':item['in_reply_to_status_id_str'],'retweet_userid':retweeted_user_id,'retweet_tweetid':retweeted_tweet_id,'like_count':item['favorite_count'],'retweet_count':item['retweet_count'],'hashtags':','.join(hashtags),'urls':','.join(urls),'user_mentions':','.join(user_mentions)})            
        return results
    
    def getItemsDF(self, ids):
        results = self.getItemsByIds(ids)
        df = pd.json_normalize(results)
        return df

if __name__ == '__main__':
    
    if len(sys.argv) >= 3:
        try:
            config['credentials']
        except:
            print('Please save your credentials into .env file')
        if 'credentials' in config:
            src = str(sys.argv[1])
            dest = str(sys.argv[2])
            if len(sys.argv) == 4 and str(sys.argv[3]) == 'False':
                isHash = False
            else:
                isHash = True
            print('Reading data from ',src)
            df = pd.read_csv(src)
            df['tweetid']=df['url'].str.split('/').str[-1]
            ids = df['tweetid'].astype(np.int64).tolist()
            df1 = df[['tweetid','accountType','added','categories','categoryDetails','checked','city','cityCode','continent','continentCode','country','countryCode','region','regionCode','locationName','engagementType','gender','impressions','insightsHashtag','insightsMentioned','interest','language','matchPositions','mediaFilter','mediaUrls','professions','queryId','queryName','reachEstimate','resourceType','sentiment','tags','threadCreated','updated','classifications','impact','imageMd5s','imageInfo']]
            print(str(len(ids)),'ids are extracted from ',src)
            print('Fetching data from Twitter ...')
            t = Twitter(isHash)
            data = t.getItemsDF(ids)
            print(str(len(df)),' items are retrieved from Twitter')
            df1.loc[:,'tweetid'] = df1.loc[:,'tweetid'].astype(np.int64)
            data.loc[:,'tweetid'] = data.loc[:,'tweetid'].astype(np.int64)
            df2 = pd.merge(data, df1, on='tweetid')
            df2.to_csv(dest,escapechar="\\", index=False)
            print('Datasets are merged and saved to ', dest)
    else:
        print('Please input source and destination file path like this,')
        print('\t python3 twitter.py <path>/brandwatch.csv <path>/twitter.csv [True|False]')
        print('* Replace <path> with the relative/absolute file path, \'brandwatch.csv\' is the file generated from brandwatch-downloader, \'twitter.csv\' is the output file, there is an optional parameter True or False for hash userid, default is True.')
        print('* Please note, csv file is using \',\' as delimiter.')
