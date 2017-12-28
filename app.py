# --------------------------------------------------
# Passbook - Web methods
# Name: Arthur Trujillo Virzin
# Date: 20/11/17
# Time: 16:01
# --------------------------------------------------

from flask import Flask
from flask import request, Response
from flapper_boarding_pass.controllers import FprBoardingPassController
import json

app = Flask(__name__)

# ---------------------------------------
# Boarding pass web methods
# ---------------------------------------


@app.route('/boarding_pass', methods=['POST'])
def get_boarding_pass():
    boarding_pass_controller = FprBoardingPassController()
    data = boarding_pass_controller.create_boarding_pass(request.json)
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


# Run Config
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)