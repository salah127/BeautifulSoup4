import requests
from pymongo import MongoClient
from fetcher import fetch_articles

def main():
    url = "https://www.blogdumoderateur.com"
    
    # Fetch articles
    articles = fetch_articles(url)
    print(f"Fetched {len(articles)} articles.")
    
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['article_db']
    collection = db['articles']
    
    # Insert articles into the collection
    if articles:
        collection.insert_many(articles)
        print(f"Inserted {len(articles)} articles into the database.")
    else:
        print("No articles fetched.")

if __name__ == "__main__":
    main()