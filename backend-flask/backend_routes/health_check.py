from flask import request, g

def load():
    @app.route('/api/health_check')
    def health_check():
        return {'Success': True}, 200