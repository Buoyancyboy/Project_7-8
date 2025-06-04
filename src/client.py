import paho.mqtt.client as mqtt

class ClientOptions:
	def __init__(self, address, port=1883, name="Broker", autodiscover=False):
		self.BROKER_ADDRESS = address
		self.BROKER_PORT = port

		self.name = name
		self.autodiscover = autodiscover

class BrokerClient:
	def __init__(self, options):
		self.CLIENT = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata=None, protocol=mqtt.MQTTv5)
		self.OPTIONS = options

		self.CLIENT.on_connect = on_connect
		self.CLIENT.on_subscribe = on_subscribe
		self.CLIENT.on_message = on_message

		self.connect_broker()

	def connect_broker(self):
		self.CLIENT.connect(self.OPTIONS.BROKER_ADDRESS, self.OPTIONS.BROKER_PORT)
		self.CLIENT.loop_start()

	def publish_message(self, topic, payload, qos=0, retain=False):
		result = self.CLIENT.publish(topic, payload, qos, retain)
		if result.rc != mqtt.MQTT_ERR_SUCCESS:
			print(f"Failed to publish message: {result.rc}")
		else:
			print(f"Message published to topic '{topic}'")

	# def discover_topics():

def on_connect(client, userdata, flags, reason_code, properties):
	if reason_code.is_failure:
		print("Cant connect: {reason_code}.")
	else:
		print("Connected")

def on_subscribe(client, userdata, mid, reason_code_list, properties):
	if reason_code_list[0].is_failure:
		print("Failed to subscribe to topic {mid}")
	else:
		print("Subscribed to topic {mid}")

def on_message(client, userdata, message):
	print("On " + message.topic + ": " + message.payload.decode())
