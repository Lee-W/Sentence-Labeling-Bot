import os

from flask_script import Manager
from flask_migrate import Migrate

from labelingbot import create_app, db


app = create_app(os.getenv('FLASKY_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    manager.run()
