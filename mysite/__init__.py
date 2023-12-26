from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
#from flask_mail import Mail
#from flask_bootstrap import Bootstrap
from mysite.config import Config
#from mysite.dash_layouts.layouts import layout
#from sqlalchemy import create_engine
#import dash
import os


#engine = create_engine('sqlite:///site.db')
#db = SQLAlchemy()
bcrypt = Bcrypt()
#bootstrap = Bootstrap()
#dash_app = dash.Dash()
#login_manager = LoginManager()
#login_manager.login_view = 'users.login'
#login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

#    db.init_app(app)
    bcrypt.init_app(app)
    #login_manager.init_app(app)
#    bootstrap = Bootstrap(app)
    # Create a Dash app within the Flask app
#    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/')
#    dash_app.layout = layout

#    from mysite.users.routes import users
#    app.register_blueprint(users)

    os.environ["OPENAI_API_KEY"] = "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"
    os.environ["HUGGINGFACE_API_KEY"] = "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"

    from mysite.main.routes import main
    app.register_blueprint(main)

    # from mysite.posts.routes import posts
    # app.register_blueprint(posts)

    from mysite.public_policies.routes import public_policies
    app.register_blueprint(public_policies)

    # from mysite.service_info.routes import services
    # app.register_blueprint(services)

    # from mysite.ai_services.opinions.routes import opinions_bp
    # app.register_blueprint(opinions_bp)

    # from mysite.opinions_plus.routes import opinions_plus
    # app.register_blueprint(opinions_plus, url_prefix='/opinions_plus')

    # from mysite.ai_services.lite_voice_generation.lvc_routes import lvc
    # app.register_blueprint(lvc, url_prefix='/ai_services/')

    return app




