from hashlib import md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s
import re, sys
import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np

user_id_dict = {}
user_name_dict = {}
user_url_dict = {}
user_screen_name_dict = {}

def getUserDetails(value, dict_type='id'):
    if dict_type == 'id':
        if value not in user_id_dict.keys():
            user_id_dict[value] = getHash(value)                
        value_hash = user_id_dict[value]
    elif dict_type == 'name':
        if value not in user_name_dict.keys():
            user_name_dict[value] = getHash(value)
        value_hash = user_name_dict[value]
    elif dict_type == 'url':
        if value not in user_url_dict.keys():
            user_url_dict[value] = getHash(value)
        value_hash = user_url_dict[value]
    elif dict_type == 'screenname':
        if value not in user_screen_name_dict.keys():
            user_screen_name_dict[value] = getHash(value)
        value_hash = user_screen_name_dict[value]
    return value_hash

def getHash(value, algo='sha1'):
    value = str(value)
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

if __name__ == '__main__':
    
    if len(sys.argv) >= 3:
            src = str(sys.argv[1])
            dest = str(sys.argv[2])
            print('Reading data from ',src)
            df = pd.read_csv(src,encoding='utf-8',low_memory=False)
            df['user_id'] = df['user_id'].apply(lambda x: getUserDetails(str(x), 'id'))
            df['title'] = df['title'].apply(lambda x: getUserDetails(str(x), 'url'))
            df['url'] = df['url'].apply(lambda x: getUserDetails(str(x), 'url'))
            df['user_profile_url'] = df['user_profile_url'].apply(lambda x: getUserDetails(str(x), 'url'))
            df['user_screen_name'] = df['user_screen_name'].apply(lambda x: getUserDetails(str(x), 'screenname'))
            df['tweet_id'] = df['tweet_id'].apply(getHash)
            df['twitter_retweet_userid'] = df['twitter_retweet_userid'].apply(getHash)
            df['twitter_retweet_tweetid'] = df['twitter_retweet_tweetid'].apply(getHash)
            df['twitter_in_reply_to_userid'] = df['twitter_in_reply_to_userid'].apply(getHash)
            df['twitter_in_reply_to_tweetid'] = df['twitter_in_reply_to_tweetid'].apply(getHash)   
            df['user_mentions'] = df['user_mentions'].apply(lambda x: ','.join([getHash(item) if item != 'nan' else '' for item in str(x).split(',')]))         
            df.to_csv(dest, escapechar="\"", encoding='utf-8', index=False)
            print('Dataset is hashed and saved to ', dest)
    else:
        print('Please input source and destination file path like this,')
        print('\t python3 hash.py <path>/raw.csv <path>/hash.csv')
        print('* Replace <path> with the relative/absolute file path, \'raw.csv\' is the file generated from fb.py or twitter.py, \'hash.csv\' is the output file.')
        print('* Please note, csv file is using \',\' as delimiter.')
