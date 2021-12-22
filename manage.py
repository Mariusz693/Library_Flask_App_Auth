from os import environ
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv
from Library_App import create_app, db

load_dotenv()

app=create_app()

app.config.from_object('config.Config')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
