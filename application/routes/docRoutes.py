from flask import request, jsonify, Blueprint
from flask_graphql import GraphQLView
from flask import current_app as app
from ..schemas.Schemas import schema

docRoutesBlueprint = Blueprint('docRoutes', __name__)

app.add_url_rule(
    '/graphql-api',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
