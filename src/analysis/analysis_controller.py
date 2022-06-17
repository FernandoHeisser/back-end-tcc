from flask_restx import Resource, fields

from src.config.server.instance import server
from src.analysis.analysis_repository import *

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
        return aprioriV2(api.payload)

