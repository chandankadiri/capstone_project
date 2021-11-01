import pymongo
import pandas as pd
from pymongo import MongoClient

def get_mongo_connection():
    try:
        client = MongoClient()
        db = client.capstone
        collection = db.news_articles
        return collection
    except Exception as err:
        raise Exception(err)

def read_from_mongo():
    try:
        collection = get_mongo_connection()
        df = pd.DataFrame(list(collection.find()))
        print(f'returned {df.shape[0]} rows from mongodb')
        return df
    except Exception as err:
        raise Exception(err)

def write_to_mongo(data):
    if isinstance(data,list):
        data = pd.DataFrame(data)
    try:
        collection = get_mongo_connection()
        collection.insert_many(data.to_dict('records'))
        print(f'inserted {data.shape[0]} rows in to mongodb')
        return True
    except Exception as err:
        raise Exception(err)

def delete_from_mongo(del_type,del_cond):
    try:
        collection = get_mongo_connection()
        if del_type=='many':
            collection.delete_many(del_cond)
        elif del_type=='all':
            collection.remove( {} )
        print('deleted  rows from  mongodb')
        return True
    except Exception as err:
        raise Exception(err)

if __name__ == '__main__':
    df = read_from_mongo()
    import pdb;pdb.set_trace()
    #delete_from_mongo('many', {'extra_col1':''})
