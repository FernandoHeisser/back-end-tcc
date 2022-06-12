from src.server.instance import server

from src.controllers.stocks import *
from src.controllers.users import *
from src.controllers.news import *
from src.controllers.analysis import *

app = server

if __name__ == '__main__':
    app.run()

