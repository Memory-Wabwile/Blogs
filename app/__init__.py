from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config_options
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail
import os



bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos',IMAGES)
mail = Mail()
#initializing application
def create_app(config_name):

    app = Flask(__name__)

    #Creating app configurations
    app.config.from_object(config_options[config_name])
    from .auth import auth as auth_blueprint
   
    #initialzing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix='/authenticate')

    # configure UploadSet
    configure_uploads(app,photos)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    return app