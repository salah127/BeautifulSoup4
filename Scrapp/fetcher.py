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
        
        ###############################################################################################
        # I added thi class_='d-flex' just to limit my article/ c'est juste pour limité les articles.#
        ###############################################################################################
        articles = soup.find_all('article', class_='d-flex')    
        for article in articles:

            meta_div = article.find('div', class_='entry-meta ms-md-5 pt-md-0 pt-3')
            tag = (meta_div.find('span', class_='favtag color-b').get_text(strip=True)) if meta_div else None

            header = (meta_div.find('header', class_='entry-header pt-1')) if meta_div else None
            a_tag = header.find('a') if header else None
            article_url = a_tag['href'] if a_tag and a_tag.has_attr('href') else None
            
            article_hat = None
            if article_url:
                try: 
                    article_response = requests.get(article_url, headers=headers)
                    article_response.raise_for_status()
                    article_soup = BeautifulSoup(article_response.text, 'html.parser')
                    
                    terms_div = article_soup.find('div', class_='article-terms')
                    Sub_Cat = None
                    if terms_div:
                        ul_tag = terms_div.find('ul')
                        Sub_Cat = ul_tag.get_text(strip=True) if ul_tag else None
                    
                    time_tag = article_soup.find('time', class_='entry-date')
                    published_date = time_tag['datetime'] if time_tag and time_tag.has_attr('datetime') else None
                    
                    byline_span = article_soup.find('span', class_='byline')
                    author_a_tag = byline_span.find('a') if byline_span else None
                    author_name = author_a_tag.get_text(strip=True) if author_a_tag else None

                    content_head = article_soup.find('header', class_='entry-header') 
                    
                    if content_head:
                        image_div = content_head.find('figure', class_='article-hat-img')
                        hat_image_tag = image_div.find('img')
                        hat_image_url = hat_image_tag['src'] if hat_image_tag and hat_image_tag.has_attr('src') else None
                        title_tag = content_head.find('h1', class_='entry-title')
                        title = title_tag.get_text(strip=True) if title_tag else None
                        hat_div = content_head.find('div', class_='article-hat')
                        article_hat = hat_div.find('p').get_text(strip=True) if hat_div else None
                    
                    
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
            articles_data.append({
                'title': title,
                'image': hat_image_url,
                'Sub_Cat': Sub_Cat,
                'article_hat': article_hat,
                'published_date': published_date,
                'author_name': author_name,
                'images': images,
                'tag': tag,
            }) 

        return articles_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []