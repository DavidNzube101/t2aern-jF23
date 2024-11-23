
import os
from flask import Flask


def initialize_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdadsadakmi23e'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__).replace('\\', '/'), 'static/upload')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    
    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')
    
    from .payments import payments
    app.register_blueprint(payments, url_prefix='/')
    
    from .admin import admin
    app.register_blueprint(admin, url_prefix='/')
    
    
    
    return app

app = initialize_app()
