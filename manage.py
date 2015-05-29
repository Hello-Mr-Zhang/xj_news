import logging

from flask import Flask, session, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CSRFProtect
from redis import StrictRedis
# 指定session保存位置
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import Config

from info import create_app, db, models

app = create_app("development")
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
