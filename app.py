# --------------------------------------------------
# Passbook - Web methods
# Name: Arthur Trujillo Virzin
# Date: 20/11/17
# Time: 16:01
# --------------------------------------------------

from flask import Flask, jsonify
from flask import request
from flapper_passbook.controllers import FprBoardingPassController

app = Flask(__name__)

# ---------------------------------------
# Boarding pass web methods
# ---------------------------------------


@app.route('/boarding_pass', methods=['POST'])
def get_boarding_pass():
    FprBoardingPassController.create_boarding_pass(request.json)
    return 'OK'


@app.route('/boarding_pass', methods=['GET'])
def create_boarding_pass():
    return 'OK'


# Run Config
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)