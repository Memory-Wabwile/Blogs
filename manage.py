from app import create_app,db
from flask_script import Manager,Server
from flask_migrate import Migrate,MigrateCommand
from app.models import User,Blogs,Comment

#Creating app instance
app = create_app('production')

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('server' , Server)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app , db = db , User = User, Blogs=Blogs , Comment=Comment)

@manager.command
def test():
    """
    Run the unit tests.
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()