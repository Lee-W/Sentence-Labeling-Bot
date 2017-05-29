import os

from flask import current_app
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from labelingbot import create_app, db
from labelingbot.models import User


def make_shell_context():
    return dict(app=current_app, db=db, User=User)


manager = Manager(create_app)
manager.add_option(
    '-c', '--config', dest='config_name',
    required=False, default=os.getenv('LABELING_BOT_CONFIG') or 'default'
)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    from labelingbot import models
    db.create_all()


if __name__ == "__main__":
    manager.run()
