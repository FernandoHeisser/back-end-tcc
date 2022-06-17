import requests, uuid
from bs4 import BeautifulSoup

from src.config.database.connection import *

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

