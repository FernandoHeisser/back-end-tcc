from src.config.server.instance import server

from src.news.news_controller import *
from src.sessions.sessions_controller import *
from src.yfinance.yfinance_controller import *
from src.stocks.stocks_controller import *
from src.users.users_controller import *
from src.analysis.analysis_controller import *

app = server

if __name__ == '__main__':
    app.run()

