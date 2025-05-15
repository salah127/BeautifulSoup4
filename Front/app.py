from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# MongoDB connection
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['article_db']
collection = db['articles']

@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html is in a 'templates' folder

@app.route('/api/articles', methods=['GET'])
def get_articles():
    query = {}
    tag = request.args.get('tag')
    author = request.args.get('author')
    search = request.args.get('search')
    
    if not tag and not author and not search:
        articles = list(collection.find({}, {'_id': 0}))
        return jsonify(articles)
 
    if tag:
        query['tag'] = tag
    if author:
        query['author_name'] = {'$regex': author, '$options': 'i'}
    if search:
        query['title'] = {'$regex': search, '$options': 'i'}

    articles = list(collection.find(query, {'_id': 0}))
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)