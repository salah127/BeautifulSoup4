import requests
from bs4 import BeautifulSoup

def fetch_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles_data = []

        main_tag = soup.find('main')
        if not main_tag:
            print("No <main> tag found.")
            return []

        articles = soup.find_all('article')
        for article in articles:
            img_div = article.find('div', class_='post-thumbnail picture rounded-img')
            img_tag = img_div.find('img') if img_div else None
            img_url = img_tag['data-lazy-src'] if img_tag and img_tag.has_attr('data-lazy-src') else None

            meta_div = article.find('div', class_='entry-meta ms-md-5 pt-md-0 pt-3')
            tag = (meta_div.find('span', class_='favtag color-b').get_text(strip=True)) if meta_div else None
            date = (meta_div.find('span', class_='posted-on t-def px-3').get_text(strip=True)) if meta_div else None

            header = (meta_div.find('header', class_='entry-header pt-1')) if meta_div else None
            a_tag = header.find('a') if header else None
            article_url = a_tag['href'] if a_tag and a_tag.has_attr('href') else None
            
            article_hat = None
            if article_url:
                try:
                    article_response = requests.get(article_url, headers=headers)
                    article_response.raise_for_status()
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    
                    hat_div = article_soup.find('div', class_='article-hat')
                    article_hat = hat_div.find('p').get_text(strip=True) if hat_div else None
                    
                    time_tag = article_soup.find('time', class_='entry-date')
                    published_date = time_tag['datetime'] if time_tag and time_tag.has_attr('datetime') else None
                    
                    byline_span = article_soup.find('span', class_='byline')
                    author_a_tag = byline_span.find('a') if byline_span else None
                    author_name = author_a_tag.get_text(strip=True) if author_a_tag else None
                    
                    images = []
                    content_div = article_soup.find('div', class_='entry-content')
                    
                    if content_div:
                        for img in content_div.find_all('img'):
                            img_url = img['src'] if img.has_attr('src') else None
                            if img_url and img_url.startswith('https'):
                                figcaption = img.find_next('figcaption')
                                img_caption = figcaption.get_text(strip=True) if figcaption else img.get('alt', None)
                                
                                images.append({
                                    'url': img_url,
                                    'caption': img_caption
                                })
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching article content: {e}")
            title = (a_tag.find('h3').get_text(strip=True)) if a_tag and a_tag.find('h3') else None
            
            Sub_Cat = (meta_div.find('span', class_='favtag color-b').get_text(strip=True)) if meta_div and meta_div.find('span', class_='favtag color-b') else None

            summary_div = (meta_div.find('div', class_='entry-excerpt t-def t-size-def pt-1')) if meta_div else None
            summary = summary_div.get_text(strip=True) if summary_div else None

            articles_data.append({
                'title': title,
                'image': img_url,
                'Sub_Cat': Sub_Cat,
                'article_hat': article_hat,
                'published_date': published_date,
                'author_name': author_name,
                'images': images,
                'tag': tag,
                'date': date,
                'url': article_url,
                'summary': summary,  
            })

        return articles_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []