from flask import Flask
from App.views import init_blueprint


def create_app():
    app = Flask(__name__)
    init_blueprint(app)
    return app