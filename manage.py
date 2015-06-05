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
from info.models import User

app = create_app("development")
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-n', '-name', dest='name')
@manager.option('-p', '-password', dest='password')
def createsuperuser(name, password):
    """创建管理员用户"""
    if not all([name, password]):
        print('参数不足')
        return

    user = User()
    user.mobile = name
    user.nick_name = name
    user.password = password
    user.is_admin = True

    try:
        db.session.add(user)
        db.session.commit()
        print("创建成功")
    except Exception as e:
        print(e)
        db.session.rollback()


if __name__ == '__main__':
    manager.run()
