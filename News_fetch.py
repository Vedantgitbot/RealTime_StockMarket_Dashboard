import requests

def get_stock_news_from_newsapi(company_name, api_key):
    # Define the endpoint
    url = 'https://newsapi.org/v2/everything'
    
    # Set parameters: company_name as query, and your API key
    params = {
        'q': company_name,  
        'apiKey':'' ,  # API key
        'language': 'en',   
        'sortBy': 'publishedAt',  
        'pageSize': 5,      
    }
    
    # Send GET request to NewsAPI
    response = requests.get(url, params=params)
    
    # Check if request is successful
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        
        # Prepare a list of articles
        news_articles = []
        for article in articles:
            title = article.get('title', 'No title available')
            publisher = article.get('source', {}).get('name', 'No publisher available')
            link = article.get('url', 'No link available')
            
            news_articles.append({
                'title': title,
                'publisher': publisher,
                'link': link
            })
        
        return news_articles
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

# Example usage:
api_key = "YOUR_NEWSAPI_KEY"
company_name = "Apple"
news_articles = get_stock_news_from_newsapi(company_name, api_key)

if news_articles:
    for idx, article in enumerate(news_articles, start=1):
        print(f"{idx}. **{article['title']}**")
        print(f"   *Publisher:* {article['publisher']}")
        print(f"   *Link:* [Read more]({article['link']})\n")
else:
    print("No news found.")
