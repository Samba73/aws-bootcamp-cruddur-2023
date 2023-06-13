from flask                              import request, g
from flask_cors                         import cross_origin

from lib.return_data                    import return_json
from lib.decode_verify_jwt              import jwt_required
from lib.return_data                    import return_json

from services.home_activities           import HomeActivities
from services.notifications_activities  import NotificationsActivities
from services.create_activity           import CreateActivity
from services.search_activities         import SearchActivities
from services.create_reply              import CreateReply


def load(app):
    def default_home_page(e):
            app.logger.debug(e)
            app.logger.debug("unauthenicated")
            data = HomeActivities.run()
            return data, 200
            
    @app.route("/api/activities/home", methods=['GET'])
    @jwt_required(on_error=default_home_page)
    def data_home():
        #  data = HomeActivities.run(LOGGER)
        #  with xray_recorder.in_subsegment('api-route'):
        data = HomeActivities.run(cognito_user_id=g.cognito_user_id)
        return data, 200
    
    @app.route("/api/activities/notifications", methods=['GET'])
    def data_notifications():
        data = NotificationsActivities.run()
        return data, 200


    @app.route("/api/activities/search", methods=['GET'])
    def data_search():
        term = request.args.get('term')
        model = SearchActivities.run(term)
        return return_json(model)

    @app.route("/api/activities", methods=['POST', 'OPTIONS'])
    @cross_origin()
    @jwt_required()
    def data_activities():
        #user_handle = 'samba'
        message             = request.json['message']
        ttl                 = request.json['ttl']
        model = CreateActivity.run(message, g.cognito_user_id, ttl)
        return return_json(model)



    @app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST', 'OPTIONS'])
    @cross_origin()
    @jwt_required()
    def data_activities_reply(activity_uuid):
        message = request.json['message']
        model = CreateReply.run(message, g.cognito_user_id, activity_uuid)
        return return_json(model)