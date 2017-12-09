# --------------------------------------------------
# Passbook - Web methods
# Name: Arthur Trujillo Virzin
# Date: 20/11/17
# Time: 16:01
# --------------------------------------------------

from flask import Flask, jsonify
from flask import request
from flapper_passbook.models import FprBoardingPass

app = Flask(__name__)

# ---------------------------------------
# Boarding pass web methods
# ---------------------------------------

@app.route('/boarding_pass', methods=['GET'])
def get_boarding_pass():
    boarding_pass = FprBoardingPass(request.json)
    boarding_pass.setup_boarding_pass_fields()
    boarding_pass.create_pass()
    return 'OK'

@app.route('/boarding_pass', methods=['POST'])
def create_boarding_pass():
    #passbook = FprPassbook(request.json)
    #passbook.save()
    return 'OK'

# Run Config
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)