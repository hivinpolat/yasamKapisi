import os

from flask import Flask,redirect,url_for,escape,render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #MongDb ayarları yapıldı.
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://localhost/yasamkapisi'
    }
    app.secret_key = 'dev'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    

    # a simple page that says hello
    @app.route('/')
    def login():
        return redirect(url_for('auth.login'))
   
    
    #Veritabanı başlatıldı.
    from . import db#database
    db.initialize_db(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
  

    return app