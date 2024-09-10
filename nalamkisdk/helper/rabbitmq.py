import pika
import pika.credentials

class RabbitMQHelper:


    def __init__(self, endpoint: str, port: int, username: str, password: str, queue: str) -> None:
        """
        Connection setup for MQTT broker.

        :param endpoint: endpoint to MQTT broker
        :param port: port of the endpoint 
        :param username: username for MQTT broker
        :param password: password for MQTT broker
        :param queue: queue for MQTT broker
        """

        self.queue = queue

        credentials = pika.PlainCredentials(username, password)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=endpoint, 
                                                               port=port, 
                                                               credentials=credentials
                                                               ))
        self.channel = self.connection.channel()
        # Declare the queue (if it doesn't already exist)
        self.channel.queue_declare(queue=queue, durable=True)
        print("MQTT Client Ready initialized")


    def write_message(self, message):
        """
        Sends/writes a message on Queue.
        :param message: message to be sent
        """
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            body=message
        )

    # def get_message(self, topic):
    #     """
    #     Subscribes to a topic and prints the message received.
    #     :param topic: name of the topic
    #     """
    #     self.client.subscribe(topic)
    #     self.client.loop_start()

    # def on_connect(self, client, userdata, flags, rc):
    #     if rc == 0:
    #         self.logger.debug("Connected to MQTT broker successfully.")
    #     else:
    #         self.logger.error(f"Connection failed with code {rc}.")

    def on_message(self, ch, method, properties, body):
        print(f"Received message: {body}")

    def listen(self, method=None):
        """
        Listens for messages.
        :param method: method to handle the message (default is self.on_message)
        """
        # Set up subscription on the queue
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback = method if method is not None else self.on_message,
            auto_ack=False
        )

        print(f"Waiting for messages in {self.queue}.")
        self.channel.start_consuming()
