import os
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask_cors import CORS, cross_origin
from flaskr.notification.Job1 import handleNotifications

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # initialize scheduler. Check for sending notifications every 5 mins (300 seconds)
    scheduler = APScheduler()
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()
    @scheduler.task('interval', id='do_job_1', seconds=300)
    def job1():
        print('Job1 Running')
        handleNotifications()
        print('Job1 Done')

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

    # relative imports of the blueprints
    from .auth import auth
    from .view import view
    from .notifications_routes import notifications

    # register blueprints to the app
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(view, url_prefix = '/')
    app.register_blueprint(notifications, url_prefix = '/')

    # Should change root page to something else after this. but leaving it as is right now.
    # root page
    @app.route('/')
    def landing():
        return render_template('index.html')
 
    return app
