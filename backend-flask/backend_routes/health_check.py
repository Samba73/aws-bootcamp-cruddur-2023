from flask import request, g

def load(app):
    @app.route('/api/health_check')
    def health_check():
        return {'Success': True}, 200

    @app.route('/rollbar/test')
    def rollbar_test():
        g.rollbar.report_message('Hello', 'warning')
        return "Hello"