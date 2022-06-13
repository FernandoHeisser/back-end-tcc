from dateutil import parser
import requests
import uuid
import re

from src.database.connection import *

def handleRequest(endpoint):
    baseUrl = "https://newsapi.org/v2"
    
    key1 = "a7573d2a661c4566bf7b6b05c5efff18"
    key2 = "cb423fcc1e9a41568373a8438d79b63f"
    key3 = "8eef55ec3ed043c595233e3a34b9038f"
    key4 = "b4c272cce7b54834be7ffcec82d8310d"
    
    url = baseUrl + endpoint

    
    response = requests.get(url + key1)
    if response.status_code == 200:
        return response
    else:
        response = requests.get(url + key2)
        if response.status_code == 200:
            return response
        else:
            response = requests.get(url + key3)
            if response.status_code == 200:
                return response
            else:
                response = requests.get(url + key4)
                return response

def findWholeWord(word, string):
    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(string) is not None

def removeDuplicates(response):
    urls = []
    articles = []

    for article in response:
        if article['url'] not in urls:
            urls.append(article['url'])
            articles.append(article)

    return articles

def getGoogleNews(search):
    if 'keywords' not in search:
        return 'BAD_REQUEST', 400

    if search['keywords'] is None or len(search['keywords']) == 0:
        return 'BAD_REQUEST', 400

    if 'sources' in search:
        sources = []
        for source in search['sources']:
            sources.append(source["value"])
    else:
        sources = []

    response = []

    keywords = search['keywords']

    if isinstance(keywords, str):
        keywords = keywords.split(', ')

    for keyword in keywords:
        response_list_headlines = fetchGoogleNewsHeadlinesByKeyword(keyword)
        response_list_everything = fetchGoogleNewsEverythingByKeyword(keyword)
        response = [*response, *response_list_headlines, *response_list_everything]

    if len(response) < 10:
        if len(keywords) != 0 and len(sources) == 0:
            response_list = getFromDatabaseByKeywords(keywords)
            response = [*response, *response_list]

        elif len(keywords) == 0 and len(sources) != 0:
            response_list = getFromDatabaseBySources(sources)
            response = [*response, *response_list]

        elif len(keywords) != 0 and len(sources) != 0:
            response_list = getFromDatabaseByKeywordsAndSources(keywords, sources)
            response = [*response, *response_list]

    if len(sources) != 0:
        filtered = []
        for article in response:
            if article['source']['name'] in sources:
                filtered.append(article)
        response = filtered

    response = removeDuplicates(response)

    return sorted(response, key = lambda article: (parser.parse(article["publishedAt"])), reverse=True)

#-- Get news from database -----------------------------------------------

def getFromDatabaseByKeywords(keywords): 
    articles = list(googleNewsDb.find({}))

    result = []
    for article in articles:
        for keyword in keywords:
            checkTitle = findWholeWord(str(keyword).lower(), str(article["title"]).lower())
            checkDescription = findWholeWord(str(keyword).lower(), str(article["description"]).lower())
            checkContent = findWholeWord(str(keyword).lower(), str(article["content"]).lower())

            if (checkTitle or checkDescription or checkContent) and article not in result:
                result.append(article)

    return sorted(result, key = lambda article: (parser.parse(article["publishedAt"])), reverse=True)

def getFromDatabaseBySources(sources):
    articles = []
    for source in list(set(sources)):
        filter = {
            "source.name": source
        }
        articles.extend(list(googleNewsDb.find(filter)))

    return sorted(articles, key = lambda article: (parser.parse(article["publishedAt"])), reverse=True)

def getFromDatabaseByKeywordsAndSources(keywords, sources):
    articles = []
    for source in list(set(sources)):
        filter = {
            "source.name": source
        }
        articles.extend(list(googleNewsDb.find(filter)))

    result = []
    for article in articles:
        for keyword in keywords:
            checkTitle = findWholeWord(str(keyword).lower(), str(article["title"]).lower())
            checkDescription = findWholeWord(str(keyword).lower(), str(article["description"]).lower())
            checkContent = findWholeWord(str(keyword).lower(), str(article["content"]).lower())


            if (checkTitle or checkDescription or checkContent) and article not in result:
                result.append(article)

    return sorted(result, key = lambda article: (parser.parse(article["publishedAt"])), reverse=True)

#-- Fetch news from Google API -------------------------------------------

def fetchGoogleNewsHeadlinesByKeyword(keyword):
    response = handleRequest(f"/top-headlines?q={keyword}&apiKey=")

    if response.status_code == 200:

        articles = response.json()['articles']
        response_list = []

        for article in articles:
            response_list.append(article)
            
            if len(list(sourcesDb.find({"value": article['source']['name']}))) == 0:
                sourcesDb.insert_one({
                    "_id": str(uuid.uuid4()),
                    "value": article['source']['name']
                })
            
            if len(list(googleNewsDb.find({"url": article['url']}))) == 0:
                article['_id'] = str(uuid.uuid4())
                googleNewsDb.insert_one(article)

    return response_list

def fetchGoogleNewsEverythingByKeyword(keyword):
    response = handleRequest(f"/everything?q={keyword}&apiKey=")

    if response.status_code == 200:
    
        articles = response.json()['articles']
        response_list = []

        for article in articles:    
            response_list.append(article)

            if len(list(sourcesDb.find({"value": article['source']['name']}))) == 0:
                sourcesDb.insert_one({
                    "_id": str(uuid.uuid4()),
                    "value": article['source']['name']
                })

            if len(list(googleNewsDb.find({"url": article['url']}))) == 0:
                article['_id'] = str(uuid.uuid4())
                googleNewsDb.insert_one(article)
    
    return response_list

