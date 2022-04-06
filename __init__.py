from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = "123556aasggett"

    from . import stracker
    app.register_blueprint(stracker.bp)
    return app