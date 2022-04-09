import json
from pathlib import Path

import mongoengine
from flask import Flask
from larksuiteoapi import Config, DOMAIN_FEISHU, DefaultLogger, LEVEL_DEBUG, LEVEL_WARN
from larksuiteoapi.service.im.v1 import Service as LarkIMService

from lark_bot_demo.util.lipsum import LipsumDatabase


def create_app(conf_file: str = "config.json"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_file(conf_file, load=json.load)
    app.config['SECRET_KEY'] = app.config["LARK"]["app_secret"]

    app.config.lark = Config.new_config_with_memory_store(
        DOMAIN_FEISHU,
        Config.new_internal_app_settings(**app.config["LARK"]),
        DefaultLogger(),
        LEVEL_DEBUG if app.config["DEBUG"] else LEVEL_WARN
    )
    app.lark_im = LarkIMService(app.config.lark)

    mongoengine.connect(**app.config["DATABASE"])

    app.lipsum = LipsumDatabase(Path(app.config.root_path) / "data" / "lipsum.txt")

    # A simple page that says hello
    @app.route('/ping')
    def hello():
        return 'Pong'

    # Register blueprints
    from lark_bot_demo.callback import view as callback_view
    app.register_blueprint(callback_view.bp)
    with app.app_context():
        callback_view.init()

    return app
