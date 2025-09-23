import pika
import pika.credentials
import ssl


class RabbitMQHelper:
    def __init__(
        self, endpoint: str, port: int, username: str, password: str, queue: str
    ) -> None:
        """
        Connection setup for MQTT broker with automatic dev/prod queue support.

        :param endpoint: endpoint to MQTT broker
        :param port: port of the endpoint
        :param username: username for MQTT broker
        :param password: password for MQTT broker
        :param queue: base queue name (dev queue auto-created as queue-dev)
        """

        self.queue = queue
        self.available_queues = []
        self.current_source_queue = None

        credentials = pika.PlainCredentials(username, password)

        context = ssl.create_default_context()
        ssl_options = pika.SSLOptions(context, server_hostname=endpoint)

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=endpoint,
                port=port,
                credentials=credentials,
                heartbeat=1200,
                ssl_options=ssl_options,
            )
        )
        self.channel = self.connection.channel()

        # Try to declare both prod and dev queues
        for queue_name in [queue, f"{queue}-dev"]:
            try:
                self.channel.queue_declare(queue=queue_name, durable=True)
                self.available_queues.append(queue_name)
                print(f"Queue {queue_name} ready")
            except Exception as e:
                print(f"WARNING: Queue {queue_name} not available: {e}")

        if not self.available_queues:
            raise Exception("No queues available - service cannot start")

        print(f"MQTT Client ready - listening on: {self.available_queues}")

    def write_message(self, message):
        """
        Sends/writes a message back to the source queue.
        Can only be called once per message processing cycle.
        :param message: message to be sent
        """
        if not self.current_source_queue:
            raise Exception(
                "write_message() called outside of message processing context or multiple times per message"
            )

        self.channel.basic_publish(
            exchange="", routing_key=self.current_source_queue, body=message
        )

        # Reset context after successful send - prevents multiple writes
        self.current_source_queue = None

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
        Listens for messages on all available queues.
        :param method: method to handle the message (default is self.on_message)
        """

        def internal_callback(ch, method_info, properties, body):
            # Set message context for response routing
            self.current_source_queue = method_info.routing_key
            # Call original callback
            callback = method if method is not None else self.on_message
            return callback(ch, method_info, properties, body)

        # Set up subscription on all available queues
        for queue in self.available_queues:
            self.channel.basic_consume(
                queue=queue, on_message_callback=internal_callback, auto_ack=False
            )

        print(f"Waiting for messages on: {self.available_queues}")
        self.channel.start_consuming()
