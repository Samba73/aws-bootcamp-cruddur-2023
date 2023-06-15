from flask                                  import request, g
from flask_cors                             import cross_origin

from lib.return_data                        import return_json
from lib.decode_verify_jwt                  import jwt_required
from lib.return_data                        import return_json

from services.messages.message_groups       import MessageGroups
from services.messages.messages             import Messages
from services.messages.create_message       import CreateMessage

def load(app):
    @app.route("/api/message_groups", methods=['GET'])
    @jwt_required()
    def data_message_groups():
        cognito_user_id = g.cognito_user_id
        app.logger.debug(cognito_user_id)
        data = MessageGroups.run(cognito_user_id=cognito_user_id)
        print('message_groups', data)
        return data, 200

    @app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
    @jwt_required()
    def data_messages(message_group_uuid):
        cognito_user_id = g.cognito_user_id
        app.logger.debug(cognito_user_id)
        model = Messages.run(cognito_user_id, message_group_uuid)
        return return_json(model)
        
    @app.route("/api/messages", methods=['POST', 'OPTIONS'])
    @cross_origin()
    @jwt_required()
    def data_create_message():
        message            = request.json['message']
        handle             =  request.json.get('handle', None)
        message_group_uuid = request.json.get('message_group_uuid', None)
            # authenicatied request
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
        return return_json(model)