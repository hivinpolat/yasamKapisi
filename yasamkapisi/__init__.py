# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:43:34 2020

@author: HP
"""
import os

from flask import Flask,redirect,url_for,escape,render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'yasamkapisi.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def login():
        return redirect(url_for('auth.login'))
   
   
    
    from . import db#database
    db.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
  

    return app