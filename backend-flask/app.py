from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os
import logging
from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.update_profile import *

## x-ray
#from aws_xray_sdk.core import xray_recorder
#from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Honeycomb
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# -- Rollbar

import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

from lib.decode_verify_jwt import extract_access_token, DecodeVerifyJWT, TokenVerifyError, jwt_required
# cloudwatch log
# import watchtower
# import logging
# from time import strftime

# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)
# LOGGER.info('Watchtower:CW Log')

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

##x-ray initialize
#xray_recorder.configure(service='backend-flask')

#XRayMiddleware(app, xray_recorder)

# Honeycomb: Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
# -- Rollbar
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')

with app.app_context():
    def init_rollbar():
        """init rollbar module"""
        rollbar.init(
            # access token
            rollbar_access_token,
            # environment name
            'production',
            # server root directory, makes tracebacks prettier
            root=os.path.dirname(os.path.realpath(__file__)),
            # flask already sets up logging
            allow_logging_basic_config=False)

        # send exceptions from `app` to rollbar, using flask's signal system.
        got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


    # @app.after_request
    # def after_request(response):
    #    timestamp = strftime('[%Y-%b-%d %H:%M]')
    #    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    #    return response

    @app.route('/rollbar/test')
    def rollbar_test():
        rollbar.report_message('Hello World!', 'warning')
        return "Hello World!"

    @app.route('/api/health_check')
    def health_check():
        return {'Success': True}, 200

    @app.route("/api/message_groups", methods=['GET'])
    @jwt_required()
    def data_message_groups():
        cognito_user_id = g.cognito_user_id
        app.logger.debug(cognito_user_id)
        data = MessageGroups.run(cognito_user_id=cognito_user_id)
        if data['errors'] is not None:
            return data['errors'], 422
        else:
            return data['data'], 200

    @app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
    @jwt_required()
    def data_messages(message_group_uuid):
        cognito_user_id = g.cognito_user_id
        app.logger.debug(cognito_user_id)
        model = Messages.run(cognito_user_id=cognito_user_id,
                        message_group_uuid=message_group_uuid)
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200

    @app.route("/api/profile/update", methods=['POST','OPTIONS'])
    @cross_origin()
    @jwt_required()
    def data_update_profile():
        bio          = request.json.get('bio',None)
        display_name = request.json.get('display_name',None)
        cognito_user_id = g.cognito_user_id
        model = UpdateProfile.run(
        cognito_user_id=cognito_user_id,
        bio=bio,
        display_name=display_name
        )
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200

    @app.route("/api/messages", methods=['POST', 'OPTIONS'])
    @cross_origin()
    @jwt_required()
    def data_create_message():
        message            = request.json['message']
        handle             =  request.json.get('handle', None)
        message_group_uuid = request.json.get('message_group_uuid', None)
            # authenicatied request
        app.logger.debug("authenicated")
        app.logger.debug(claims)
        cognito_user_id = g.cognito_user_id
        app.logger.debug(cognito_user_id)
        if handle:
            model = CreateMessage.run(trans='new',
                                    cognito_user_id=cognito_user_id,
                                    message=message, handle=handle)
        else:
            model = CreateMessage.run(trans='update',
                                    cognito_user_id=cognito_user_id,
                                    message=message, message_group_uuid=message_group_uuid)                            
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200

    def default_home_page(e):
        app.logger.debug(e)
        app.logger.debug("unauthenicated")
        data = HomeActivities.run()
        
    @app.route("/api/activities/home", methods=['GET'])
    @jwt_required(on_error=default_home_page)
    def data_home():
        #  data = HomeActivities.run(LOGGER)
        #  with xray_recorder.in_subsegment('api-route'):
        app.logger.debug("authenicated")
        app.logger.debug(claims)
        data = HomeActivities.run(cognito_user_id=g.cognito_user_id)

    @app.route("/api/activities/notifications", methods=['GET'])
    def data_notifications():
        data = NotificationsActivities.run()
        return data, 200

    @app.route("/api/activities/@<string:handle>", methods=['GET'])
    def data_handle(handle):
        model = UserActivities.run(handle)
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200

    @app.route("/api/activities/search", methods=['GET'])
    def data_search():
        term = request.args.get('term')
        model = SearchActivities.run(term)
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200
        return

    @app.route("/api/activities", methods=['POST', 'OPTIONS'])
    @cross_origin()
    @jwt_required()
    def data_activities():
        #user_handle = 'samba'
        message             = request.json['message']
        ttl                 = request.json['ttl']
        model = CreateActivity.run(message, g.cognito_user_id, ttl)
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200

    @app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
    @jwt_required()
    def data_show_activity(activity_uuid):
        data = ShowActivity.run(activity_uuid=activity_uuid)
        return data, 200

    @app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST', 'OPTIONS'])
    @cross_origin()
    @jwt_required()
    def data_activities_reply(activity_uuid):
        message = request.json['message']
        model = CreateReply.run(message, g.cognito_user_id, activity_uuid)
        if model['errors'] is not None:
            return model['errors'], 422
        else:
            return model['data'], 200
        return


    if __name__ == "__main__":
        app.run(debug=True)
