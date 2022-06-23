import requests
from dateutil import parser
from bs4 import BeautifulSoup

def extractedNews(tags):
    try:
        base_url = 'https://news.google.com'
        html = requests.get(f'{base_url}/search?for={tags}&hl=pt-BR&gl=BR', headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}).content
        soup = BeautifulSoup(html, 'html.parser')
        div_list = soup.find("div", {"class": "lBwEZb BL5WZb xP6mwf"}).contents
        
        main_div_list = []
        article_div_list = []

        for div in div_list:
            if ' '.join(div['class']) == 'NiLAwe mi8Lec gAl5If jVwmLb Oc0wGc R7GTQ keNKEd j7vNaf nID9nc':
                main_div_list.append(div)
            else:
                article_div_list.append(div)

        main_articles = []
        for main_div in main_div_list:
            try:
                try:
                    main_article_image = main_div.div.div.a.figure.img['srcset']
                except:
                    print('Error getting main_article_image')
                    main_article_image = None

                try:
                    main_article_url = str(main_div.div.div.article.h3.a['href']).replace('.', base_url)
                except:
                    print('Error getting main_article_url')
                    main_article_url = None
                
                try:
                    main_article_title = main_div.div.div.article.h3.a.string
                except:
                    print('Error getting main_article_title')
                    main_article_title = None
                
                try:
                    main_article_source_url = str(main_div.div.div.article.div.div.a['href']).replace('.', base_url)
                except:
                    main_article_source_url = None
                
                try:
                    main_article_source_title = main_div.div.div.article.div.div.a.string
                except:
                    print('Error getting main_article_source_title')
                    main_article_source_title = None
                    
                try:
                    main_article_time_date = main_div.div.div.article.div.div.time['datetime']
                except:
                    print('Error getting main_article_time_date')
                    main_article_time_date = '2000-01-01T00:00:00Z'
                    
                try:
                    main_article_time_title = main_div.div.div.article.div.div.time.string
                except:
                    print('Error getting main_article_time_title')
                    main_article_time_title = None

                m_article = {
                    'image': str(main_article_image),
                    'url': str(main_article_url),
                    'title': str(main_article_title),
                    'source': {
                        'url': str(main_article_source_url),
                        'title': str(main_article_source_title)
                    },
                    'time': {
                        'date': str(main_article_time_date),
                        'title': str(main_article_time_title)
                    }
                }

                try:
                    main_article_div_list = main_div.div.div.find("div", {"class": "SbNwzf eeoZZ"}).contents
                except:
                    print('Error getting main_article_div_list')
                    main_article_div_list = []

                sub_articles = []
                for article_div in main_article_div_list:
                    try:
                        sub_article_url = str(article_div.h4.a['href']).replace('.', base_url)
                    except:
                        print('Error getting sub_article_url')
                        sub_article_url = None
                    try:
                        sub_article_title = str(article_div.h4.a.string)
                    except:
                        print('Error getting sub_article_title')
                        sub_article_title = None
                    try:
                        sub_article_source_url = str(article_div.div.a['href']).replace('.', base_url)
                    except:
                        sub_article_source_url = None
                    try:
                        sub_article_source_title = str(article_div.div.a.string)
                    except:
                        print('Error getting sub_article_source_title')
                        sub_article_source_title = None
                    try:
                        sub_article_time_date = str(article_div.div.time['datetime'])
                    except:
                        print('Error getting sub_article_time_date')
                        sub_article_time_date = '2000-01-01T00:00:00Z'
                    try:
                        sub_article_time_title = str(article_div.div.time.string)
                    except:
                        print('Error getting sub_article_time_title')
                        sub_article_time_title = None

                    sub_articles.append({
                        'url': sub_article_url,
                        'title': sub_article_title,
                        'source': {
                            'url': sub_article_source_url,
                            'title': sub_article_source_title
                        },
                        'time': {
                            'date': sub_article_time_date,
                            'title': sub_article_time_title
                        }
                    })

                first_sub_article = sub_articles[0]
                del sub_articles[0]
                
                main_articles.append({
                    'article': m_article,
                    'firstSubArticle': first_sub_article,
                    'subArticles': sub_articles
                })
            except:
                print('Error getting main article')
                return None

        articles = []
        for article_div in article_div_list:
            if ' '.join(article_div['class']) == 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc':
                try:
                    article_image = article_div.a.figure.img['srcset']
                except:
                    print('Error - article_image')
                    article_image = None
                try:
                    article_title = article_div.div.article.h3.a.string
                except:
                    print('Error - article_title')
                    article_title = None
                try:
                    article_url = str(article_div.div.article.h3.a['href']).replace('.', base_url)
                except:
                    print('Error - article_url')
                    article_url = None
                try:
                    article_source_title = article_div.div.article.div.div.a.string
                except:
                    print('Error - article_source_title')
                    article_source_title = None
                try:
                    article_source_url = str(article_div.div.article.div.div.a['href']).replace('.', base_url)
                except:
                    article_source_url = None
                try:
                    article_time_title = article_div.div.article.div.div.time.string
                except:
                    print('Error - article_time_title')
                    article_time_title = None
                try:
                    article_time_date = str(article_div.div.article.div.div.time['datetime'])
                except:
                    print('Error - article_time_date')
                    article_time_date = '2000-01-01T00:00:00Z'

                articles.append({
                    'image': article_image,
                    'title': article_title,
                    'url': article_url,
                    'source': {
                        'title': article_source_title,
                        'url': article_source_url
                    },
                    'time': {
                        'title': article_time_title,
                        'date': article_time_date
                    }
                })

            if ' '.join(article_div['class']) == 'NiLAwe y6IFtc R7GTQ keNKEd j7vNaf':
                try:
                    article_title = article_div.div.article.h3.a.string
                except:
                    print('Error - article_title')
                    article_title = None
                try:
                    article_url = str(article_div.div.article.h3.a['href']).replace('.', base_url)
                except:
                    print('Error - article_url')
                    article_url = None
                try:
                    article_source_title = article_div.div.article.div.div.a.string
                except:
                    print('Error - article_source_title')
                    article_source_title = None
                try:
                    article_source_url = str(article_div.div.article.div.div.a['href']).replace('.', base_url)
                except:
                    article_source_url = None
                try:
                    article_time_title = article_div.div.article.div.div.time.string
                except:
                    print('Error - article_time_title')
                    article_time_title = None
                try:
                    article_time_date = str(article_div.div.article.div.div.time['datetime'])
                except:
                    print('Error - article_time_date')
                    article_time_date = None
                
                articles.append({
                    'image': None,
                    'title': article_title,
                    'url': article_url,
                    'source': {
                        'title': article_source_title,
                        'url': article_source_url
                    },
                    'time': {
                        'title': article_time_title,
                        'date': article_time_date
                    }
                })
        
        ordered_articles = sorted(articles, key = lambda article: (parser.parse(article["time"]["date"])), reverse=True)

        return {
            'mainArticles': main_articles,
            'articles': ordered_articles
        }
    except:
        print('Error - extractedNews')
        return None

def isValidTags(tags):
    if tags is None:
        return False

    if tags == '':
        return False
    
    if len(tags.split('+')) <= 0:
        return False
    
    return True

def getNews(tags):
    if isValidTags(tags):
        return extractedNews(tags)