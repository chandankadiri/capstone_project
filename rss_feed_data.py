import feedparser
from dateutil import parser as date_parser

def collect_rss_feed_data():
    articles_list = []
    NewsFeed = feedparser.parse("https://timesofindia.indiatimes.com/rssfeedstopstories.cms")
    for entry in NewsFeed.entries:
        title = entry['title']
        published_date = str(date_parser.parse(entry['published'][:-4]))
        summary = entry['summary']
        source_link = entry['link']
        source = entry['link'].split('/')[2]
        topic = entry['link'].split('/')[3]
        article_dict = {'title':title,'published_date':published_date,'summary':summary,'topic':topic,'source':source,'source_link':source_link,
                'load_type':'rssfeed','extra_col1':'','extra_col2':''}
        articles_list.append(article_dict)
        #print(article_dict)
    return articles_list


if __name__ == '__main__':
    collect_rss_feed_data()

    
