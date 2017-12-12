# --------------------------------------------------
# Classes FprBoardingPass,
# Name: Arthur Trujillo Virzin
# Date: 26/11/17
# Time: 21:39
# --------------------------------------------------

from jsonschema import Draft3Validator
from wallet.models import Pass, Barcode, BoardingPass, BarcodeFormat
from config import Config
import random, string
import json
import sys
import os


class FprBoardingPass(BoardingPass):

    # Constructor
    def __init__(self, json):

        BoardingPass.__init__(self)
        self.schema = self.init_schema()

        # TODO: Implement cool validation
        # if Draft3Validator(self.schema).is_valid(json):
        #     self.init_boarding_pass(json);
        # else:
        #     print("Invalid JSON.")
        #     raise ImportError

        #self.init_boarding_pass(json)

        #Config
        self.config = Config()

        self.init_boarding_pass(json)

        # Header
        self.request_body = None
        self.relevant_date = None
        self.locations = None
        self.message = None

        #Fields
        self.flight_number = None
        self.departing_time = None
        self.boarding_time = None
        self.departure_place = None
        self.departure_code = None
        self.arrival_place = None
        self.arrival_code = None
        self.seats_qty = None
        self.aircraft_prefix = None
        self.aircraft_model = None
        self.operator_name = None
        self.passengers = [Passenger, ]
        self.departure_details = None

    def init_boarding_pass(self, json):
        """

        :param json:
        """
        obj = json.loads(json)
        self.flight_number = obj.flightNumber
        self.relevant_date = obj.boardingTime
        self.set_locations(json.locations)
        self.departure_place = obj.departurePlace
        self.departure_code = obj.departureCode
        self.arrival_place = obj.arrivalPlace
        self.arrival_code = obj.arrivalCode
        self.aircraft_prefix = obj.aircraftPrefix
        self.aircraft_model = obj.aircraftModel
        self.operator_name = obj.operatorName
        self.set_passengers(json.passengers)
        self.departure_details = obj.departureDetails

    def set_locations(self, locations):
        for location in locations:
            self.locations.append(Location(location.latitude, location.longitude))

    def set_passengers(self, passsengers):
        for passenger in passsengers:
            self.passengers.append(Passenger(passenger.fullName, passenger.documents))

    def setup_boarding_pass_fields(self):
        self.addHeaderField('boardingTime', self.boarding_time, 'BOARDING TIME')
        self.addPrimaryField('departurePlace',self.departure_code, self.departure_place)
        self.addPrimaryField('arrivalPlace', self.arrival_code, self.arrival_place)
        self.addSecondaryField('passenger', self.passengers[0].full_name, 'PASSENGER')
        self.addAuxiliaryField('departingTime', self.departing_time, 'DEPARTURE')
        self.addAuxiliaryField('seats', self.seats_qty, 'SEATS')
        self.addAuxiliaryField('prefix', self.aircraft_prefix, 'PREFIX')
        self.addAuxiliaryField('operator', self.operator_name, 'OPERATOR')
        self.addBackField('aircraft', self.aircraft_model, 'AIRCRAFT')
        self.add_passengers()
        self.addBackField('departureDetails', self.departure_details, 'DEPARTURE DETAILS')

    def create_pass(self):
        passfile = Pass(self, passTypeIdentifier=self.config.PASS_TYPE_IDENTIFIER,
                        organizationName=self.config.ORGANIZATION_NAME,
                        teamIdentifier=self.config.TEAM_IDENTIFIER)
        passfile.serialNumber = self.get_serial_number()
        passfile.relevantDate = self.relevant_date
        passfile.barcode = Barcode(message='blablabla e372438427y4 dahsdgasidhas lasgdiavdajsdjba',
                                   format=BarcodeFormat.QR)
        passfile.addFile('icon.png', open(r'/opt/project/flapper_passbook/icon.png', 'rb'))
        passfile.addFile('icon@2x.png', open(r'/opt/project/flapper_passbook/icon@2x.png', 'rb'))
        passfile.addFile('logo.png', open(r'/opt/project/flapper_passbook/logo.png', 'rb'))
        passfile.addFile('logo@2x.png', open(r'/opt/project/flapper_passbook/logo@2x.png', 'rb'))
        passfile.foregroundColor = "rgb(255, 255, 255)"
        passfile.backgroundColor = "rgb(38, 29, 62)"
        passfile.labelColor = "rgb(13, 179, 163)"
        passfile.create(self.config.PROJECT_PATH + '/certificates/certificate.pem',
                        self.config.PROJECT_PATH + '/certificates/key.pem',
                        self.config.PROJECT_PATH + '/certificates/wwdr.pem',
                        self.config.PASSFILE_PASSWORD,
                        self.config.PROJECT_PATH + '/opt/project/flapper_passbook/test.pkpass')

    def get_serial_number(self,
                          size=9,
                          chars=string.ascii_uppercase+string.digits+string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_barcode(self):
        barcode_string = self.departure_code + self.arrival_code + " "\
                         + self.passengers[0].full_name\
                         + " " + self.flight_number + " " + self.departing_time
        return barcode_string

    def add_passengers(self):
        if len(self.passengers) > 0:
            passengers_details = None
            for passenger in self.passengers:
                passengers_details += passenger.full_name + '\n'
                for document in passenger.documents:
                    passengers_details += document.type + '\n'
            passengers_details += '\n'
            self.addBackField('passengers', passengers_details, 'PASSENGERS')


class FprPass(Pass):

    # Constructor
    def __init__(self):
        self.config = Config()
        Pass.__init__(self, passTypeIdentifier=self.config.PASS_TYPE_IDENTIFIER, organizationName=self.config.ORGANIZATION_NAME,
                      teamIdentifier=self.config.TEAM_IDENTIFIER)
        self.serialNumber = self.get_serial_number()
        self.barcode = Barcode(message=barcode, format=BarcodeFormat.QR)
        self.addFile('icon.png', open(r'/opt/project/flapper_passbook/icon.png', 'rb'))
        self.addFile('icon@2x.png', open(r'/opt/project/flapper_passbook/icon@2x.png', 'rb'))
        self.addFile('logo.png', open(r'/opt/project/flapper_passbook/logo.png', 'rb'))
        self.addFile('logo@2x.png', open(r'/opt/project/flapper_passbook/logo@2x.png', 'rb'))
        self.foregroundColor = "rgb(255, 255, 255)"
        self.backgroundColor = "rgb(38, 29, 62)"
        self.labelColor = "rgb(13, 179, 163)"

    def get_serial_number(self,
                          size=9,
                          chars=string.ascii_uppercase+string.digits+string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def get_pass_filename(self):
        pass

    def generate(self):
        self.create(self.config.PROJECT_PATH + '/certificates/certificate.pem',
                    self.config.PROJECT_PATH + '/certificates/key.pem',
                    self.config.PROJECT_PATH + '/certificates/wwdr.pem',
                    self.config.PASSFILE_PASSWORD,
                    self.config.PROJECT_PATH + '/opt/project/flapper_passbook/test.pkpass')

    # TODO:call boto3
    def save(self):
        return 1


class Passenger():

    # Constructor
    def __init__(self, full_name, documents):
        self.full_name = full_name
        self.documents = [Document, ]
        self.set_documents(documents)

    def set_documents(self, documents):
        for doc in documents:
            self.documents.append(Document(doc.type, doc.number))


class Document():

    # Constructor
    def __init__(self, type, number):
        self.type = type
        self.number = number


class Location():

    # Constructor
    def __init__(self, latitude=None, longitude=None):
        self.latitude = latitude
        self.longitude = longitude
