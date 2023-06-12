from flask                      import request, g

from lib.return_data            import return_json
from lib.decode_verify_jwt      import jwt_decoder
from lib.return_data            import return_json

from services.show_activity     import *
from services.update_profile    import *
from services.user_activities   import *

def load():
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
        return(return_json(model))
        
    
    @app.route("/api/activities/@<string:handle>", methods=['GET'])
    def data_handle(handle):
        model = UserActivities.run(handle)
        return(return_json(model))
        
    
    @app.route("/api/activities/@<string:handle>/status/<string:activity_uuid>", methods=['GET'])
    @jwt_required()
    def data_show_activity(handle, activity_uuid):
        data = ShowActivity.run(handle, activity_uuid=activity_uuid)
        return(return_json(data))        