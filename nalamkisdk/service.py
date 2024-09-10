import os
import shutil
import traceback
import json
import dataclasses

from .helper import RabbitMQHelper, MinIOHelper

from .model.action import Action, S3Bucket
from .model.encoder import NaLamKIDataEncoder

prod_action_path    = os.path.join("action")
test_action_path    = os.path.join("test","action")

class NaLamKIService:

    def __init__(self):
        self.model = self.init_model()
        self.s3 = None
        self.action_path = prod_action_path
        self.rmq = RabbitMQHelper(os.getenv('MQTT_HOST'), os.getenv('MQTT_PORT'), os.getenv('MQTT_USERNAME'), os.getenv('MQTT_Password'), os.getenv('MQTT_QUEUE'))

    def init_model(self):
        '''
        Initialize the AI Model
        '''
        # initialize the Model
        return None

    def load_inputData(self):
        '''
        Helper: Load input Data from input directory.
        '''
        path = os.path.join(self.action_path, "input")
        input_files = []
        for file in os.listdir(path):
            input_files.append(open(os.path.join(path, file), 'rb'))
        return input_files
    
    def save_data(self, files):
        '''
        Helper: Save list of files in output directory. 
        '''
        path = os.path.join(self.action_path, "output")
        for file in files:
            with open(os.path.join(path, os.path.basename(file.name)), 'w') as f:
                f.write(file.read())

    def process_data(self):
        pass

    def on_message(self, ch, method, properties, body):
        '''
        On revice message parse message and do actions. 
        '''
        try:
            action = Action.from_json(body)
            if action.pattern == "start":
                self.do_action(action=action)
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as error:
            print("ERROR: MQTT Message cannot be executed")
            print(error)
            traceback.print_exc() 
            print(body)
            self.rmq.write_message(json.dumps(dataclasses.asdict(Action(pattern="ERROR", data=None)), cls=NaLamKIDataEncoder))
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def do_action(self, action:Action):
        '''
        Excecute Service for Action. 
        '''
        # Create temp Action directory and download files
        if os.path.exists(self.action_path):
           self.delete_action_content()
        # self.delete_action_content()
        self.create_action_content()
        self.get_action_data(action)
        # Do the calculation
        self.process_data()
        # Upload the final Data and delete the temp Directory
        self.upload_action_data(action) 
        # Inform digital Twin about finishing
        self.send_finish_message(action)

    def local_test(self):
        '''
        Set path to test directory and run Process without loading data from S3. 
        '''
        self.action_path = test_action_path
        self.process_data()
        self.action_path = prod_action_path


    def run(self):
        while True:
            # try:
            print("Service Loop started")
            self.rmq.listen(self.on_message)
            # except Exception as e:
            #     print("Error: %s : %s" % (e.strerror))
            # print("Ooups an error occured")

    def create_action_content(self):
        '''
        Create required Action Directory for current run.
        '''
        os.makedirs(self.action_path, exist_ok=True)
        os.makedirs(os.path.join(self.action_path, "input"), exist_ok=True)
        os.makedirs(os.path.join(self.action_path, "output"), exist_ok=True)

    def delete_action_content(self):
        '''
        Delete teporal action directory. 
        '''
        try:
            shutil.rmtree(os.path.join(self.action_path, "input"))
            shutil.rmtree(os.path.join(self.action_path, "output"))
        except OSError as e:
            print("Error: %s : %s" % (self.action_path, e.strerror))

    def get_action_data(self, action:Action):
        '''
        Get Action Data from S3 Storage.
        '''
        bucket = action.data.bucket
        self.s3 = MinIOHelper(bucket.endpoint, bucket.accessId, bucket.accessToken, bucket.name)

        # Get Input Object Names
        files = []
        for inputFile in action.data.inputData:
            if self.s3.is_directory(inputFile):
                files.extend(self.s3.list_file_object_names(recursive=True, prefix=inputFile))
            elif(self.s3.object_exists(inputFile)):
                files.append(inputFile)

        for file in files:
            self.s3.download_File(file, os.path.join(self.action_path, "input", os.path.basename(file)))
    
    def upload_action_data(self, action:Action):
        '''
        Upload final data from output directory in target directory in action.
        '''
        path = os.path.join(self.action_path, "output")
        for file in os.listdir(path):
            self.s3.upload_File(file_path= os.path.join(path, file), object_file=os.path.join(action.data.outputData, file))

    def send_finish_message(self, action:Action):
        print('EMIT FINISH')
        action.pattern = "finish"
        print(json.dumps(dataclasses.asdict(action)))
        self.rmq.write_message(json.dumps(dataclasses.asdict(action), cls=NaLamKIDataEncoder))