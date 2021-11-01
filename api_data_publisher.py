#!/usr/bin/python3                                                                                                      
                                                                                                                        
from kafka import KafkaProducer                                                                                         
from random import randint                                                                                              
from time import sleep                                                                                                  
import sys,json       
import pandas as pd
from api_data import collect_api_data
BROKER = 'localhost:9092'                                                                                               
TOPIC = 'news_artcles'                                                                                                      
#BROKER = 'broker:29092'
#TOPIC = 'pageviews'
                                                                                                                       
import pdb;pdb.set_trace()
try:                                                                                                                    
    p = KafkaProducer(bootstrap_servers=BROKER)                                                                         
except Exception as e:                                                                                                  
    print(f"ERROR --> {e}")                                                                                             
    sys.exit(1)                                                                                                        
                                                                                                                        
#while True:
#    articles = collect_api_data()
#    for article in articles:       
#        article = json.dumps(article).encode('utf-8')
#        print(article)
#        p.send(TOPIC, value=article)   
#    print('sleeping 10secs')
#    sleep(5)
#
prev_top_news = {'title':''}
while True:
    articles = collect_api_data()
    if prev_top_news['title'] == articles[0]['title']:
        print('No news articles published to kafka')
        sleep(600)
    else:
        for article in articles:
            if article != prev_top_news['title']:
                import pdb;pdb.set_trace()
                article = json.dumps(article).encode('utf-8')
                print(article)
                p.send(TOPIC, value=article)
                print('published to kafka. sleeping 5 secs... ')
                sleep(5)
            else:
                break

    prev_top_news = articles[0]
