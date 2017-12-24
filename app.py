# --------------------------------------------------
# Passbook - Web methods
# Name: Arthur Trujillo Virzin
# Date: 20/11/17
# Time: 16:01
# --------------------------------------------------

from flask import Flask, jsonify
from flask import request
from flapper_boarding_pass.controllers import FprBoardingPassController

app = Flask(__name__)

# ---------------------------------------
# Boarding pass web methods
# ---------------------------------------


@app.route('/boarding_pass', methods=['POST'])
def get_boarding_pass():
    boarding_pass_controller = FprBoardingPassController()
    boarding_pass_controller.create_boarding_pass(request.json)
    return 'OK'


# Run Config
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)