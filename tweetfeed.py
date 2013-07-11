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


api = twitter.Api(consumer_key='XXXXXXXXX',
                      consumer_secret='XXXXXXXXXXXX',
                      access_token_key='XXXXXXXXXXXXXX',
                      access_token_secret='XXXXXXXXXXXX')

friends = api.GetFriends()
rss = PyRSS2Gen.RSS2(
    title = "Vanderloos PyRSS2Gen feed",
    link = "http://twitter.com/van_der_loos",
    description = "The latest tweets from vanderloos' friends",

    lastBuildDate = datetime.datetime.now(),

    items = [])
statuses_sum = []

for f in friends[:5]:
	statuses_sum += api.GetUserTimeline(f.id)
statuses_sum.sort(key=lambda tweet: tweet.created_at_in_seconds, reverse=True)

for tweet in statuses_sum:
	item = PyRSS2Gen.RSSItem(title = printRow(tweet.user.name + ': ' + tweet.text))
	tweet_url = r'https://twitter.com/' + tweet.user.screen_name + r'/status/' + str(tweet.id)
	if tweet.in_reply_to_status_id:
		item.description = r'In reply to: https://twitter.com/' + tweet.in_reply_to_screen_name + r'/status/' + str(tweet.in_reply_to_status_id)
	if tweet.urls:
		item.link = tweet.urls[0].expanded_url

	item.guid = PyRSS2Gen.Guid(tweet_url)
	item.pubDate = tweet.created_at
	item.author = printRow(tweet.user.name)
         
	rss.items.append(item)	

twitter_statuses.close()
rss.write_xml(open("pyrss2gen.xml", "w"))
