# --------------------------------------------------
# Class FprBoardingPassController
# Name: Arthur Trujillo Virzin
# Date: 26/11/17
# Time: 21:39
# --------------------------------------------------

from flapper_boarding_pass.models import FprBoardingPass, FprPass, FprResponse
from jsonschema import Draft4Validator
from config import Config
import json


class FprBoardingPassController:

    def create_boarding_pass(self, json_content):
        """

        :param json_content: Request body as Python object
        """
        response = FprResponse()
        if self.is_schema_valid(json_content):
            boarding_pass = FprBoardingPass(json_content)
            flapper_pass = FprPass(boarding_pass)
            flapper_pass.generate()
            response.set_result(True)
            flapper_pass.save_to_s3()
            response_data = response.content_body
        else:
            response.set_result(False)
            response_data = response.content_body
        return response_data



    @staticmethod
    def is_schema_valid(json_content):
        """

        :param json_content: Request body as Python object
        :return: Boolean if JSON is valid
        """
        is_json_valid = False
        config = Config()
        schema = json.loads(open(config.PROJECT_PATH + 'schemas/create_boarding_pass.json').read())
        if Draft4Validator(schema).is_valid(json_content):
            is_json_valid = True
        return is_json_valid
