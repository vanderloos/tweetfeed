# -*- coding: utf-8 -*-
import twitter
import datetime
import PyRSS2Gen


def printRow(string):
    '''Fixing encoding issues'''
    a = format(string)

    if hasattr(a, '__unicode__'):
        a = unicode(a)

    if not isinstance(a, unicode):
        a = a.decode('utf8', 'replace')
    a = a.encode('utf8', 'replace')
    return a


class MyFeed:
    def __init__(self, consumer_key='', consumer_secret='', access_token_key='77175560-', access_token_secret='',
                 xml_out_file="pyrss2gen.xml"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token_key = access_token_key
        self.access_token_secret = access_token_secret
        self.statuses_file = ""
        self.title = "Vanderloos PyRSS2Gen feed"
        self.link = "http://twitter.com/van_der_loos"
        self.description = "The latest tweets from vanderloos' friends"
        self.xml_out_file = xml_out_file

    def get_feed(self):
        api = twitter.Api(self.consumer_key, self.consumer_secret, self.access_token_key, self.access_token_secret)

        friends = api.GetFriends()
        rss = PyRSS2Gen.RSS2(self.title, self.link, self.description,
                             lastBuildDate=datetime.datetime.now(), items=[])
        if self.statuses_file:
            twitter_statuses = open(self.statuses_file, 'w')
            twitter_statuses.write('')
            twitter_statuses.close()
            twitter_statuses = open(self.statuses_file, 'a')
        statuses_sum = []

        for friend in friends:
            statuses_sum += api.GetUserTimeline(user_id=friend.id, since_id=357931428379500544)
        statuses_sum.sort(key=lambda tweet: tweet.created_at_in_seconds, reverse=True)

        for tweet in statuses_sum:
            item = PyRSS2Gen.RSSItem(title=printRow(tweet.user.name + ': ' + tweet.text))
            tweet_url = r'https://twitter.com/' + tweet.user.screen_name + r'/status/' + str(tweet.id)
            if tweet.in_reply_to_status_id:
                item.description = r'In reply to: https://twitter.com/' + tweet.in_reply_to_screen_name + r'/status/' + str(
                    tweet.in_reply_to_status_id)
            if tweet.urls:
                item.link = tweet.urls[0].expanded_url

            item.guid = PyRSS2Gen.Guid(tweet_url)
            item.pubDate = tweet.created_at
            item.author = printRow(tweet.user.name)

            rss.items.append(item)
            if self.statuses_file:
                twitter_statuses.write(printRow(tweet.user.name) + '\n')
                twitter_statuses.write(printRow(tweet.text) + '\n')

        rss.write_xml(open(self.xml_out_file, "w"))
        if self.statuses_file:
            twitter_statuses.close()


def get_feed():
    a = MyFeed()
    a.get_feed()
