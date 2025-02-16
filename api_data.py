import requests
from pprint import pprint

def collect_api_data():
    url = "https://free-news.p.rapidapi.com/v1/search"
    
    querystring = {"q":"sport || economics || business || gaming || entertainment || politics || tech || world ","lang":"en",}
    
    headers = {
        'x-rapidapi-host': "free-news.p.rapidapi.com",
        'x-rapidapi-key': "483e4d7751msh49fcc411348658fp1bf1b8jsn3f87d88fe804"
        }
    articles_list = []
    response = requests.request("GET", url, headers=headers,params=querystring)
    import pdb;pdb.set_trace() 
    if response.status_code != 200:
        print(response.status_code)
        pprint(response.json())
        raise Exception('api call failed.. ')
    else:
        news_info = response.json()
        for page in range(1,news_info['total_pages']+1):
            querystring['page']= page
            response = requests.request("GET", url, headers=headers,params=querystring)
            if response.status_code != 200:
                print(response.status_code)
                pprint(response.json())
                raise Exception('api call failed.. ')
            else:
                articles = news_info['articles']
                articles_list = []
                for article in articles:
                    title = article['title']
                    published_date = article['published_date']
                    summary = article['summary']
                    topic = article['topic']
                    source = article['clean_url']
                    source_link = article['link']
                    #article_dict = {'title':title,'published_date':published_date,'summary':summary,'topic':topic,'source':source,'source_link':source_link,
                    #        'load_type':'rapidapi','extra_col1':'','extra_col2':''}
                    article_dict = {'text':summary,'category':topic,}
                    print(50*'#*#')
                    pprint(article_dict)
                    articles_list.append(article_dict)
                    import time;time.sleep(1)
    return articles_list


if __name__ == '__main__':
    collect_api_data()
    
