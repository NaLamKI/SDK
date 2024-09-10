import pika
import logging
import os

class RabbitMQHelper:
    """
    Helper class for establishing connection to RabbitMQ. 

    A request/reply pattern is implemented.
    """

    def __init__(self, endpoint:str, port:int ,routing_key:str, username:str, password:str, path:str ="") -> None:

        """
        connection setup RabbitMQ 

        :param endpoint: endpoint to RabbitMQ ( withot http\https)
        :param port: port of the endpoint 
        :param routing_key: the routing key for send the Message  

        """
        
        logging.basicConfig(format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

        try:
            self.credentials_intern = pika.PlainCredentials(username, password)
            self.connection_paramters = pika.ConnectionParameters(endpoint,port,"/",self.credentials_intern)
            self.connection = pika.BlockingConnection(self.connection_paramters)
            self.channel = self.connection.channel()
            # self.channel.queue_declare(routing_key,durable=True)
            self.channel.queue_bind(routing_key)
            self.logger.debug("Connection to RabbitMQ successful.")
        except Exception as exp:
            self.logger.error(f"Connection error to RabbitMQ. \n Message: {exp}")

        self.queue = routing_key
        self.sending_message_back = True
        self.f = None
        self.args = None
        self.path = path
        self.messag = None 

    def check_and_create_path(self):
        if(not os.path.exists(self.path)):
            os.makedirs(self.path)

    def write_message(self,queue, messag):
        """
        sends/write an message on the queue  

        :param queue: name of the queue
        :param messag: message to be sent
        """
        # self.channel.queue_declare(queue)
        self.channel.basic_publish(exchange='', routing_key = queue, body=messag)

    def get_message(self, queue):
        method_frame, header_frame, body = self.channel.basic_get('test')
        if method_frame:
            print(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
        else:
            print('No message returned')

    def on_message(self, channel, method_frame, header_frame, body):
        print(method_frame.delivery_tag)
        print(body)
        print()
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    
    def listen(self, queue, method=None):
        self.channel = self.connection.channel()
        if method is None:
            method = self.on_message
        self.channel.basic_consume(queue, method)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.connection.close()

