from newsapi import NewsApiClient

api = NewsApiClient(api_key='c8391cf9562243678c0dfbe459074133')


print(api.get_top_headlines(sources='bbc-news'))