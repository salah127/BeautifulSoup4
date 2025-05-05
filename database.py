from pymongo import MongoClient

def get_db_connection(uri, db_name):
    client = MongoClient(uri)
    return client[db_name]

def insert_article(db, collection_name, article_data):
    collection = db[collection_name]
    collection.insert_one(article_data)