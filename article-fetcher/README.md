# Article Fetcher

## Overview
Article Fetcher is a Python application that fetches articles from a specified URL and saves the article information into a MongoDB collection. It utilizes the BeautifulSoup library for web scraping and pymongo for database interactions.

## Project Structure
```
article-fetcher
├── src
│   ├── main.py          # Entry point of the application
│   ├── fetcher.py       # Contains the function to fetch articles
│   ├── database.py      # Handles MongoDB connection and data insertion
│   └── utils
│       └── __init__.py  # Utility functions and constants
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd article-fetcher
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your MongoDB database and update the connection details in `src/database.py`.

## Usage

1. Run the application:
   ```
   python src/main.py
   ```

2. The application will fetch articles from the specified URL and save them to the MongoDB collection.

## Dependencies
- requests
- beautifulsoup4
- pymongo

## Contributing
Feel free to submit issues or pull requests for improvements or bug fixes.