from src.config.server.instance import server

from stocks.stocks_controller import *
from users.users_controller import *
from analysis.analysis_controller import *

app = server

if __name__ == '__main__':
    app.run()

