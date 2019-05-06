#encoding:utf-8
#专门用来写命令的文件

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app
from exts import db
from models import User,Question

manager=Manager(app)

#使用Migrate绑定db和app
migrate=Migrate(app,db)

#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()
