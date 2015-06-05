import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CSRFProtect
from flask.ext.session import Session
from flask.ext.wtf.csrf import generate_csrf
from redis import StrictRedis

from config import config


db = SQLAlchemy()
redis_store = None  # type: StrictRedis


# redis_store: StrictRedis = None


def setup_log(config_name):
    # 设置日志记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    # 创建日志记录器，指明日志记录保存的路径，每个日志文件的最大大小，保存的日志文件个数上限
    file_log_handler = RotatingFileHandler('logs/log', maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式，日志等级， 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask APP 使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    setup_log(config_name)
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # db = SQLAlchemy(app)
    db.init_app(app)
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT,
                              decode_responses=True)

    # 开启csrf保护,已经做了校验功能
    CSRFProtect(app)
    from info.utils.common import do_index_class
    app.add_template_filter(do_index_class, "index_class")

    @app.after_request
    def after_request(response):
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token", csrf_token)
        return response
    # 在app注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)
    from info.modules.news import news_blu
    app.register_blueprint(news_blu)
    from info.modules.profile import profile_blu
    app.register_blueprint(profile_blu)
    from info.modules.admin import admin_blu
    app.register_blueprint(admin_blu)

    # 设置session保存位置
    Session(app)
    return app
