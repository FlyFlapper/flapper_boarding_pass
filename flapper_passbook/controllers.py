# --------------------------------------------------
# Class FprBoardingPassController
# Name: Arthur Trujillo Virzin
# Date: 26/11/17
# Time: 21:39
# --------------------------------------------------


class FprBoardingPassController():

    # Constructor
    def __init__(self):
        self.full_name = None
        self.documents = [Document()]

    def init_schema(self):
        schema = {
                  "flightNumber": "495",
                  "boardingTime": "",
                  "boardingLocation": {
                    "longitude": -22.908055,
                    "latitude": -43.164189
                  },
                  "departurePlace": "Congonhas",
                  "departureCode": "SBSP",
                  "arrivalPlace": "Jacarepaguá",
                  "arrivalCode": "SBJR",
                  "departureTime": "18:00",
                  "qtySeats": 1,
                  "aircraftPrefix": "PT-MJD",
                  "operatorName": "Icon Aviation",
                  "passengerName": "John Doe",
                  "aircraftModel": "King Air B200",
                  "documents":[{
                    "label": "RG",
                    "value": "9999999-X"
                    },
                    {
                    "label": "CPF",
                    "value": "999.999.999-99"
                    }],
                  "departureDetails": "Aeroporto de Congonhas\nLounge da Icon Aviation\nAv. Jurandir, 856 - Jardim Cecy, São Paulo - SP, 04072-000\nhttps://goo.gl/maps/WPqFM3VuQHz"
                }
        return schema

    def is_json_valid(self,json_body):
        is_valid = False
        is_valid = Draft3Validator(self.schema).is_valid(json_body)
        return is_valid