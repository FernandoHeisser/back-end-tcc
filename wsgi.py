from src.config.server.instance import server

from src.stocks.stocks_controller import *
from src.users.users_controller import *
from src.analysis.analysis_controller import *

if __name__ == '__main__':
    server.run()
