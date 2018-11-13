from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from Information import create_app,db
from Information import models


app = create_app("develop")
manager = Manager(app)
Migrate(app, db)
manager.add_command("mysql", MigrateCommand)


# 入口函数
if __name__ == '__main__':
    manager.run()
