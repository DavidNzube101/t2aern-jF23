
import os
from flask import Flask, render_template


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
    
    @app.errorhandler(500)
    def internal_server_error(e, err_code=500):
        app.logger.error(f"Internal Server Error: {e}")
        return render_template('errorpage.html', error=e, code=err_code), 500

    @app.errorhandler(404)
    def route_not_found(e, err_code=404):
        app.logger.error(f"Route Not Found: {e}")
        return render_template('errorpage.html', error=e, code=err_code), 404
    
    return app
