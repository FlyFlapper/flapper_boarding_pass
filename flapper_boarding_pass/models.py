# --------------------------------------------------
# Classes FprBoardingPass,
# Name: Arthur Trujillo Virzin
# Date: 26/11/17
# Time: 21:39
# --------------------------------------------------

from wallet.models import Pass, Barcode, BoardingPass, BarcodeFormat, Alignment
from config import Config
import random
import string
import datetime
import dateutil.parser
import boto3
import os


class FprBoardingPass(BoardingPass):

    # Constructor
    def __init__(self, json_content):
        """

        :param json_content: Request content as Python object
        """
        BoardingPass.__init__(self)

        self.config = Config()

        # Fields
        self.relevant_date = None
        self.locations = []
        self.full_name = None
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
        self.passengers = []
        self.departure_details = None
        self.barcode = None

        # Initializes properties
        self.__init_boarding_pass(json_content)

    def __init_boarding_pass(self, json_content):
        """
        Fills object properties using received request
        :param json_content: Request content as Python object
        """
        self.flight_number = json_content.get('flightNumber')
        self.relevant_date = json_content.get('boardingTime')
        self.__set_locations(json_content.get('locations'))
        self.departure_place = json_content.get('departurePlace')
        self.departure_code = json_content.get('departureCode')
        self.arrival_place = json_content.get('arrivalPlace')
        self.arrival_code = json_content.get('arrivalCode')
        self.aircraft_prefix = json_content.get('aircraftPrefix')
        self.aircraft_model = json_content.get('aircraftModel')
        self.operator_name = json_content.get('operatorName')
        self.__set_passengers(json_content.get('passengers'))
        self.departure_details = json_content.get('departureDetails')
        self.seats_qty = len(self.passengers)
        self.__set_barcode()
        self.__set_boarding_time()
        self.__set_full_name()
        self.__set_departing_time()

        self.__setup_boarding_pass_fields()


    def __set_locations(self, locations):
        """
        Fills Locations property
        :param locations: locations list
        """
        for location in locations:
            self.locations.append(Location(location.get('latitude'), location.get('longitude')))

    def __set_passengers(self, passsengers):
        """
        Fills Passengers property
        :param passsengers:
        """
        for passenger in passsengers:
            self.passengers.append(Passenger(passenger.get('fullName'), passenger.get('documents')))

    def __set_full_name(self):
        """
        Sets (primary) Passenger full name
        """
        self.full_name = self.passengers[0].full_name

    def __set_boarding_time(self):
        """
        Sets boarding time property
        """
        self.boarding_time = (dateutil.parser.parse(self.relevant_date) -
                              datetime.timedelta(minutes=30)).strftime('%H:%M %d/%m')

    def __set_departing_time(self):
        """
        Sets departing time property
        """
        self.departing_time = (dateutil.parser.parse(self.relevant_date)).strftime('%H:%M')

    def __set_barcode(self):
        """
        Generates barcode string from another properties:
        - Departure code;
        - Arrival code;
        - Passenger full name;
        - Flight date in
        """
        self.barcode = self.departure_code + self.arrival_code + " "\
                       + self.passengers[0].full_name\
                       + " " + self.flight_number + " " + self.relevant_date

    def __setup_boarding_pass_fields(self):
        """
        Sets up the fields to generate boarding pass
        """
        self.addHeaderField('boardingTime', self.boarding_time, 'BOARDING TIME')
        self.addPrimaryField('departurePlace',self.departure_code, self.departure_place)
        self.addPrimaryField('arrivalPlace', self.arrival_code, self.arrival_place)
        self.addSecondaryField('passenger', self.passengers[0].full_name, 'PASSENGER')
        #TODO: Fix this ugliest workaround
        self.primaryFields[1].textAlignment = Alignment.RIGHT
        self.addAuxiliaryField('departingTime', self.departing_time, 'DEPARTURE')
        self.addAuxiliaryField('seats', self.seats_qty, 'SEATS')
        self.addAuxiliaryField('prefix', self.aircraft_prefix, 'PREFIX')
        self.addAuxiliaryField('operator', self.operator_name, 'OPERATOR')
        self.addBackField('aircraft', self.aircraft_model, 'AIRCRAFT')
        self.add_passengers()
        self.addBackField('departureDetails', self.departure_details, 'DEPARTURE DETAILS')

    @staticmethod
    def set_serial_number(size=9,
                          chars=string.ascii_uppercase+string.digits+string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def add_passengers(self):
        """
        Adds passengers to boarding pass object (list of objects)
        """
        if len(self.passengers) > 0:
            passengers_details = ""
            for passenger in self.passengers:
                passengers_details += passenger.full_name + '\n'
                for document in passenger.documents:
                    passengers_details += document.type + ': ' + document.number + '\n'
                passengers_details += '\n'
            self.addBackField('passengers', passengers_details, 'PASSENGERS')

        Initializes Flapper pass from Boarding Pass object
class FprPass(Pass):

    # Constructor
    def __init__(self, boarding_pass):
        """
        Initializes Flapper pass from Boarding Pass object
        :param boarding_pass:
        """
        self.config = Config()
        Pass.__init__(self,
                      boarding_pass,
                      passTypeIdentifier=self.config.PASS_TYPE_IDENTIFIER,
                      organizationName=self.config.ORGANIZATION_NAME,
                      teamIdentifier=self.config.TEAM_IDENTIFIER)
        self.serialNumber = self.       Gets serial number __get_serial_number()
        self.file_name = self.__get_pass_file_name(boarding_pass.relevant_date,
                                                   boarding_pass.flight_number,
                                                   boarding_pass.full_name)
        self.folder_name = (datetime.datetime.now()).strftime('%Y%m%d')
        self.barcode = Barcode(message=boarding_pass.barcode, format=BarcodeFormat.QR)
        self.addFile('icon.png', open(self.config.IMAGES_PATH + '/icon.png', 'rb'))
        self.addFile('icon@2x.png', open(self.config.IMAGES_PATH + '/icon@2x.png', 'rb'))
        self.addFile('logo.png', open(self.config.IMAGES_PATH + '/logo.png', 'rb'))
        self.addFile('logo@2x.png', open(self.config.IMAGES_PATH + '/logo@2x.png', 'rb'))
        self.foregroundColor = self.config.COLOR_FOREGROUND
        self.backgroundColor = self.config.COLOR_BACKGROUND
        self.labelColor = self.config.COLOR_LABEL

    def __get_serial_number(self,
                            size=9,
                            chars=string.ascii_uppercase+string.digits+string.ascii_lowercase):
        """
        Gets random serial number
        :param size: Number of characters
        :param chars: Characters allowed
        :return: Returns a valid random serial number for boarding pass
        """
        return ''.join(random.choice(chars) for _ in range(size))

    def __get_pass_file_name(self, date, flight_number, full_name):
        """
        Generates boarding pass name
        :param date: Flight date
        :param flight_number: Flight number
        :param full_name: Full name of the passenger
        :return:
        """
        filename = (dateutil.parser.parse(date)).strftime('%Y%m%d')
        filename += '_' + str(flight_number)
        filename += '_' + (full_name.replace(' ', '_')).lower() + '.pkpass'
        return filename

    def generate(self):
        """
        Generates .pkpass file
        :return: Returns created file
        """
        return self.create(self.config.CERTIFICATES_PATH + '/certificate.pem',
                           self.config.CERTIFICATES_PATH + '/key.pem',
                           self.config.CERTIFICATES_PATH + '/wwdr.pem',
                           self.config.PASSFILE_PASSWORD,
                           self.config.FILES_OUTPUT + '/' + self.file_name)

    def save_to_s3(self):
        """
        Saves .pkpass to Amazon S3
        """
        client = boto3.client(
            's3',
            aws_access_key_id=self.config.AWS_ACCESS_KEY,
            aws_secret_access_key=self.config.AWS_SECRET_KEY
        )
        with open(self.config.FILES_OUTPUT + '/' + self.file_name, 'rb') as data:
            client.upload_fileobj(data, self.config.S3_BUCKET_NAME, self.folder_name + '/' + self.file_name,
                                  ExtraArgs={'ACL': 'public-read'})
        os.remove(self.config.FILES_OUTPUT + '/' + self.file_name)
        print(self.file_name + 'was saved to ' + self.config.S3_BUCKET_NAME + '/' + self.folder_name + '.')

# ---------------------------------------
# Aux Classes
# ---------------------------------------


class Passenger:

    # Constructor
    def __init__(self, full_name, documents):
        """
        Creates Passenger object
        :param full_name: Passenger's full name
        :param documents: Paggenger's documents (list of Document objects)
        """
        self.full_name = full_name
        self.documents = []
        self.set_documents(documents)

    def set_documents(self, documents):
        """
        Fills documents property
        :param documents: List of objects obtained from request
        """
        for doc in documents:
            self.documents.append(Document(doc.get('type'), doc.get('number')))


class Document:

    # Constructor
    def __init__(self, type, number):
        """
        Creates Document object
        :param type: Document type
        :param number: Document number
        """
        self.type = type
        self.number = number


class Location:

    # Constructor
    def __init__(self, latitude=None, longitude=None):
        """
        Creates Location object
        :param latitude: latitude
        :param longitude: longitude
        """
        self.latitude = latitude
        self.longitude = longitude
