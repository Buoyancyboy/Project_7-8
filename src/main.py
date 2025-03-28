import client as c
import time

BROKER_URL = "localhost"

OPTIONS = c.ClientOptions(BROKER_URL,name="Broker1")
CLIENT = c.BrokerClient(OPTIONS)

CLIENT.CLIENT.subscribe("#")

while (True):
	time.sleep(3)