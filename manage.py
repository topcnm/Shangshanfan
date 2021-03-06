# coding=utf-8
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from webapp import create_app
from webapp.extension import db
from webapp.model import Article, Author
from prepare import InitManager
import os


env = os.getenv('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.{}Config'.format(env.capitalize()))
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)
manager.add_command('tag', InitManager)


@manager.shell
def get_shell_context():
    return dict(app=app, Article=Article, Author=Author)


if __name__ == '__main__':
    manager.run()
