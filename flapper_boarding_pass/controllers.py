# --------------------------------------------------
# Class FprBoardingPassController
# Name: Arthur Trujillo Virzin
# Date: 26/11/17
# Time: 21:39
# --------------------------------------------------

from flapper_boarding_pass.models import FprBoardingPass, FprPass


class FprBoardingPassController():

    @staticmethod
    def create_boarding_pass(json_body):
        boarding_pass = FprBoardingPass(json_body)
        flapper_pass = FprPass(boarding_pass)
        flapper_pass.generate()
        #flapper_pass.save_to_s3()

