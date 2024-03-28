import os
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    # relative imports of the blueprints
    from .auth import auth
    from .view import view
    from .notifications import notifications
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
