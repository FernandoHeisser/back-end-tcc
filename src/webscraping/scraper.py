from datetime import datetime
from bs4 import BeautifulSoup

import requests, uuid

from src.database.connection import *

def getArticleByUrl(stock, url):
    try:
        html = requests.get(url).content

        soup = BeautifulSoup(html, 'html.parser')    

        container = soup.find("article")

        subdivs = container.find_all("div", {"class": "layout-container"})

        subject = subdivs[0].div.find("div", {"class": "single__hat spacing--mb3"}).span.string
        title = subdivs[0].div.find("div", {"class": "single__title spacing--mb3"}).h1.string
        subtitle = subdivs[0].div.find("div", {"class": "single__excerpt typography__body--2 spacing--mb4"}).p.string
        date = subdivs[0].div.find("div", {"class": "single__author-info"}).find("span", {"class": "typography__body--6"}).time["datetime"]

        divImage = soup.find("div", {"class": "imds__aspect-ratio-overlay"})
        imageUrl = None
        if divImage is not None:
            imageUrl = divImage.img["src"]

        articleContent = subdivs[1].div.find("div", {"class": "single__content"}).div

        bigString = ''

        for p in articleContent.find_all("p"): 
            if p.string is None:   
                bigString += str(p.text)
            else:
                bigString += str(p.string)

        article = {
            "_id": str(uuid.uuid4()),
            "symbol": stock["symbol"],
            "company": stock["company"],
            "articleUrl": url,
            "subject": str(subject).strip(),
            "title": title,
            "subtitle": subtitle,
            "date": date,
            "imageUrl": imageUrl,
            "articleContent": bigString
        }

        return article
    except:
        print('Error - getArticleByUrl - ' + url)
        return None

def fetchStockNews(symbol):
    try:
        stock = stocksDb.find_one({"symbol": str(symbol).upper()})
    except:
        print('Database connection failed - getStockNews()')

    if stock is None:
        return "NOT_FOUND", 404

    try:
        html = requests.get(stock['url']).content

        soup = BeautifulSoup(html, 'html.parser')

        content = soup.find("div", {"class": "items"})

        divs = content.find_all("div", {"class": "row py-3 item"})

        articles = []

        for div in divs:
            try:
                url = div.find("div", {"class": "col-12 col-lg-4 img-container"}).a['href']
                
                article = getArticleByUrl(stock, url)
                
                if article is not None:
                    articles.append(article)
                    news = stockNewsDb.find({"$and": [{"articleUrl": article['articleUrl']},{ "symbol": article['symbol']}]})
                    if len(list(news)) == 0:
                        stockNewsDb.insert_one(article)

            except:
                continue

        return 200
    except:
        print('Error - getStockNews()')
        return 500

def fetchStockData(symbol):
    try:
        stock = stocksDb.find_one({"symbol": str(symbol).upper()})
    except:
        print('Database connection failed - getCurrentStockData()')
        return "SERVER_ERROR", 500

    if stock == None:
        return "NOT_FOUND", 404

    try:
        stockObject = {}
        stockObject["_id"] = str(uuid.uuid4())
        stockObject["company"] = str(stock['company']).strip()
        stockObject["symbol"] = str(stock['symbol']).strip()

        html = requests.get(stock['url']).content
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find("div", {"class": "quotes-header-info"})

        if div is not None:
        
            subdiv = div.find("div", {"class": "sub-header"})

            if subdiv is not None and subdiv.div is not None and subdiv.div.span is not None and subdiv.div.span.string is not None:
                dateString = subdiv.div.span.string

                try:
                    dateString = dateString.replace(' ', '').replace('\n', '').replace('às', '-').replace('h', ':')
                    stockObject["date"] = str(datetime.strptime(dateString[10:24], '%d/%m/%y-%H:%M').isoformat())
                    
                except:
                    try:
                        dateString = dateString.replace(' ', '').replace('\n', '').replace('às', '-').replace('h', ':')
                        today = str(datetime.today().date()) + dateString
                        stockObject["date"] = str(datetime.strptime(today[0:16], "%Y-%m-%d-%H:%M").isoformat())
                    except:
                        try:
                            today = str(datetime.today().date()) +"-"+ dateString[11:16]
                            stockObject["date"] = str(datetime.strptime(today, '%Y-%m-%d-%H:%M').isoformat())
                        except:
                            print('Get Date Failed ')
                        
            try:    
                subdiv2 = div.find("div", {"class": "line-info"})

                stockObject["close"] = subdiv2.find("div", {"class": "value"}).p.string
                stockObject["high"] = subdiv2.find("div", {"class": "maximo"}).p.string
                stockObject["low"] = subdiv2.find("div", {"class": "minimo"}).p.string
                stockObject["volume"] = subdiv2.find("div", {"class": "volume"}).p.string
                stockObject["variation"] = subdiv2.find("div", {"class": "percentage"}).p.string.replace(' ', '').replace('\n', '')
            except:
                stockObject["close"] = None
                stockObject["high"] = None
                stockObject["low"] = None
                stockObject["volume"] = None
                stockObject["variation"] = None

        if stockObject is not None:
            try:
                stockDataDb.insert_one(stockObject)
            except:
                print('Database connection failed - getCurrentStockData()')

        return stockObject, 200
    except:
        print('Error - fetchStockData()')
        return 500

def fetchStocks():
    try:
        html = requests.get("https://www.infomoney.com.br/cotacoes/empresas-b3/").content
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all("table", {"class": "default-table"})

        for table in tables:
            trs = table.tbody.find_all("tr")
            for tr in trs:
                stockCompany = tr.find("td", {"class": "higher"})
                stockSymbols = tr.find_all("td", {"class": "strong"})
                for stockSymbol in stockSymbols:
                    
                    url = str(stockSymbol.a['href']).strip()
                    
                    if url.lower().find(str("fii").lower()) == -1:
                        stock = {
                            "_id": str(uuid.uuid4()),
                            "company": str(stockCompany.string).strip(),
                            "symbol": str(stockSymbol.a.string).strip(),
                            "url": url
                        }
                        stocks = stocksDb.find({"symbol": stock["symbol"]})
                        if len(list(stocks)) == 0 and stock["symbol"] is not None:
                            stocksDb.insert_one(stock)
        return 200                        
    except:
        print('Error - fetchStocks()')
        return 500

