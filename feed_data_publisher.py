#!/usr/bin/python3                                                                                                      
                                                                                                                        
from kafka import KafkaProducer
from random import randint
from time import sleep
import sys,json
import pandas as pd
from rss_feed_data import collect_rss_feed_data
BROKER = 'localhost:9092'
TOPIC = 'news_artcles'

try:
    p = KafkaProducer(bootstrap_servers=BROKER)                                                                         
except Exception as e:                                                                                                  
    print(f"ERROR --> {e}")                                                                                             
    sys.exit(1)                                                                                                        
#article = b"{'title':''}"             
prev_top_news = {'title':''}
while True:
    articles = collect_rss_feed_data()
    if prev_top_news['title'] == articles[0]['title']:
        print('No news articles published to kafka')
        sleep(600)
    else:
        for article in articles:
            if article != prev_top_news['title']:
                article = json.dumps(article).encode('utf-8')
                print(article)
                p.send(TOPIC, value=article)   
                print('published to kafka. sleeping 5 secs... ')
                sleep(5)
            else:
                break
            
    prev_top_news = articles[0]
