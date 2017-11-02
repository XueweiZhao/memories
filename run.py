from flask import Flask, make_response, render_template

from routes.index import blueprint as index_blueprint
from routes.memories import blueprint as memories_blueprint


def page_not_found(error):
    return make_response(render_template('not-found.jinja'), 404)


def create_app():
    app = Flask(__name__)

    app.register_blueprint(index_blueprint)
    app.register_blueprint(memories_blueprint)
    app.register_error_handler(404, page_not_found)

    return app

