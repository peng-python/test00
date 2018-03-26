from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from company import app
from exts import db
from models import UserModel,NewsModel,AdvertisementModel


manager = Manager(app)


migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()