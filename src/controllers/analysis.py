from flask_restx import Resource, fields
import pandas_datareader as pdr
from src.server.instance import server
from src.finance.yfinance import *

app, api = server.app, server.api

input = api.model('search', {
    'stocks': fields.List,
    'startDate': fields.String,
    'endDate': fields.String,
    'minSupport': fields.Float,
    'minConfidence': fields.Float,
    'minLift': fields.Float,
    'minLength': fields.Integer,
    'firstCondition': fields.String,
    'secondCondition': fields.String
})

@api.route('/apriori')
@api.expect(input)
class Apriori(Resource):
    def post(self, ):
        try:
            return aprioriV2(api.payload)
        except:
            print('Apriori Error')
            return "ERROR", 500

@api.route('/smoke')
class Smoke(Resource):
    def get(self, ):
        return "OK", 200
