from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import json

BROKER = 'localhost:9092'
TOPIC = 'news_artcles'
client = MongoClient('localhost:27017')
collection = client.capstone.news_articles
consumer = KafkaConsumer(TOPIC,bootstrap_servers=['localhost:9092'],auto_offset_reset='earliest',enable_auto_commit=True,
        value_deserializer=lambda x: loads(x.decode('utf-8')))

while True:
    try:
        records = consumer.poll(60 * 1000) # timeout in millis , here set to 1 min
        record_list = []
        for tp, consumer_records in records.items():
            for consumer_record in consumer_records:
                collection.insert_one(consumer_record.value)
                print('{} added to mongodb {}'.format(consumer_record.value, collection))
                record_list.append(consumer_record.value)
        print(record_list) # record_list will be list of dictionaries
    except Exception as err:
        print(err)
        raise Exception(err)

        
