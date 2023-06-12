from flask              import Flask
from flask              import request, g

from lib.cloudwatch     import init_cloudwatch
from lib.honeycomb      import init_honeycomb
from lib.cors           import init_cors
from lib.rollbar        import init_rollbar

import backend_routes.activities
import backend_routes.messages
import backend_routes.users
import backend_routes.health_check

app = Flask(__name__)

# initilization
init_honeycomb(app)
init_cors(app)

# error logging in rollbar
with app.app_context():

    g.rollbar = init_rollbar(app)

# backend routes
backend_routes.health_check.load(app)
backend_routes.users.load(app)    
backend_routes.activities.load(app)
backend_routes.messages.load(app)


if __name__ == "__main__":
    app.run(debug=True)
