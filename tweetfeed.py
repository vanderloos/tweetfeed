# -*- coding: utf-8 -*-
import datetime

from twitter import *
import PyRSS2Gen



class Config:
    def __init__(self, config_path):
        self.config = open(config_path,'r')

        def conf_value(line):
            return line.split('=')[1].strip()

        for line in self.config:
            value = conf_value(line)
            if line.startswith('consumer_key'):
                self.consumer_key = value
            elif line.startswith('consumer_secret'):
                self.consumer_secret = value
            elif line.startswith('access_token_key'):
                self.access_token_key = value
            elif line.startswith('access_token_secret'):
                self.access_token_secret = value
            elif line.startswith('user_id'):
                self.user_id = value


class MyFeed:
    def __init__(self, config_path="config", xml_out_file="pyrss2gen.xml"):
        self.config = Config(config_path)
        self.statuses_file = ""
        self.title = "Vanderloos PyRSS2Gen feed"
        self.link = "http://twitter.com/van_der_loos"
        self.description = "The latest tweets from vanderloos' friends"
        self.xml_out_file = xml_out_file

    def get_feed(self,num=50):
        api = Twitter(auth=OAuth(self.config.access_token_key,
                          self.config.access_token_secret, self.config.consumer_key, self.config.consumer_secret))

        rss = PyRSS2Gen.RSS2(self.title, self.link, self.description,
                             lastBuildDate=datetime.datetime.now(), items=[])
        if self.statuses_file:
            twitter_statuses = open(self.statuses_file, 'w')
            twitter_statuses.write('')
            twitter_statuses.close()
            twitter_statuses = open(self.statuses_file, 'a')
        statuses_sum = api.statuses.home_timeline(count=num)

        statuses_sum.sort(key=lambda tweet: tweet['created_at'], reverse=False)

        for tweet in statuses_sum:
            item = PyRSS2Gen.RSSItem(title=tweet['user']['name'] + ': ' + tweet['text'])
            tweet_url = r'https://twitter.com/' + tweet['user']['screen_name'] + r'/status/' + tweet['id_str']
            if tweet['in_reply_to_status_id']:
                item.description = str(r'In reply to: <a href=https://twitter.com/' + tweet['in_reply_to_screen_name'] + r'/status/' + tweet['in_reply_to_status_id_str'] + '>' + tweet['in_reply_to_screen_name'] + '</a>')
            else: item.description = tweet_url
            if tweet['entities']['urls']:
                item.link = tweet['entities']['urls'][0]['expanded_url']

            item.guid = PyRSS2Gen.Guid(tweet_url)
            item.pubDate = tweet['created_at']
            item.author = tweet['user']['name']

            rss.items.append(item)
            '''if self.statuses_file:
                twitter_statuses.write(tweet['user']['name']) + '\n'
                twitter_statuses.write(tweet['text']) + '\n'
			'''
        rss.write_xml(open(self.xml_out_file, "w"), encoding = 'utf-8')
        if self.statuses_file:
            twitter_statuses.close()


def feed(config, out):
    a = MyFeed(config_path=config, xml_out_file=out)
    a.get_feed()
    return 'Success'
