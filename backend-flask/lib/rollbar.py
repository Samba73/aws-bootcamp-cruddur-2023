from flask import got_request_exception
import os
import rollbar
import rollbar.contrib.flask

def _get_flask_request():
    print("Gettingflask request")
    from flask import request
    print("rollbar request:", request)
    return request
rollbar._get_flask_request = _get_flask_request

def _build_request_data(request):
    return rollbar._build_werkzeug_request_data(request)
rollbar._build_request_data = _build_request_data    

def init_rollbar(app):
    """init rollbar module"""
    rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
    flask_env = os.getenv('FLASK_ENV')
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        flask_env,
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
    return rollbar