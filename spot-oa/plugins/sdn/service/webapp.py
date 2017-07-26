if __name__=='__main__':
    import sys
    from os import path

    sys.path.append(path.dirname(__file__))
    # sys.path.append(os.path.join(os.path.dirname(__file__)))

from flask import Flask, Blueprint
from flask_graphql import GraphQLView
import os

from schema import SDNSchema

app = Flask(__name__)

blueprint = Blueprint('sdn_api', __name__)
blueprint.add_url_rule('/sdn', strict_slashes=False, view_func=GraphQLView.as_view('sdn', schema=SDNSchema, graphiql=os.environ.get('SPOT_DEV') == '1'))

app.register_blueprint(blueprint)

if __name__=='__main__':
    port = int(sys.argv[1]) if len(sys.argv)>1 else 8889

    app.run(host='0.0.0.0', port=port)

def load_jupyter_server_extension(nb_app):
    import tornado.web
    import tornado.wsgi
    import sys
    from os import path   
    
    sys.path.append(path.dirname(path.dirname(__file__)))  
    print sys.path 
    from resources.osc import populateWidget

    populateWidget()

    wsgi_app = tornado.wsgi.WSGIContainer(app)
    nb_app.web_app.add_handlers(r'.*', [
        (r'/sdn.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))
    ])

    nb_app.log.info('Apache Spot SDN extension loaded')
    if os.environ.get('SPOT_DEV')=='1':
        nb_app.log.warn('Apache Spot SDN running in dev mode (environment var SPOT_DEV=1)')
