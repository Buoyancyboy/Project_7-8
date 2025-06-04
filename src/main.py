import client as c
import time
<<<<<<< HEAD
import sqlite3

BROKER_URL = "broker"
DB_FILE = "/app/data/mqtt.db"

def setup_database():
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()

    # 1. module_config
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS module_config (
            module_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_module TEXT NOT NULL UNIQUE,
            metadata TEXT
        )
    ''')

    # 2. topic_config
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topic_config (
            topic_config_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_name TEXT NOT NULL,
            data_type TEXT,
            description TEXT
        )
    ''')

    # 3. module_topic_in
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS module_topic_in (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            module_ID INTEGER,
            topic_config_ID INTEGER,
            FOREIGN KEY (module_ID) REFERENCES module_config(module_id),
            FOREIGN KEY (topic_config_ID) REFERENCES topic_config(topic_config_ID)
        )
    ''')

    # 4. module_topic_out
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS module_topic_out (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            module_ID INTEGER,
            topic_config_ID INTEGER,
            FOREIGN KEY (module_ID) REFERENCES module_config(module_id),
            FOREIGN KEY (topic_config_ID) REFERENCES topic_config(topic_config_ID)
        )
    ''')

    # 5. log_data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS log_data (
            log_data_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            topic_config_ID INTEGER NOT NULL,
            date_logged DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_config_ID) REFERENCES topic_config(topic_config_ID)
        )
    ''')

    con.commit()
    con.close()
    
def setup_module_config(description):
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()
    # Module name wordt afgeleid van de metadata van het topic
    cursor.execute("SELECT name_module FROM module_config WHERE metadata = ?", (description,))
    result = cursor.fetchone()
    if not result:
        # Voeg module toe aan module_config als deze nog niet bestaat
        cursor.execute("INSERT INTO module_config (name_module) VALUES (?)", (description,))
        con.commit()
    con.close()

def log_message_to_log_data(topic, message):
    description = "test" # Placeholder voor de beschrijving. DIT IS EEN TO DO
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()
    # Zoek het topic_config_ID op basis van topic_name
    cursor.execute("SELECT topic_config_ID FROM topic_config WHERE topic_name = ?", (topic,))
    result = cursor.fetchone()
    if result:
        topic_config_id = result[0]
    else:
        # Voeg topic toe aan topic_config als deze nog niet bestaat
        cursor.execute("INSERT INTO topic_config (topic_name, description) VALUES (?, ?)", (topic, description))
        topic_config_id = cursor.lastrowid
        con.commit()
    # Voeg bericht toe aan log_data
    cursor.execute(
        "INSERT INTO log_data (message, topic_config_ID, date_logged) VALUES (?, ?, datetime('now', '+2 hours'))",
        (message, topic_config_id)
    )
    con.commit()
    con.close()
    setup_module_config(description)

def onmessage(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")
    log_message_to_log_data(message.topic, message.payload.decode())

def get_messages_from_db():
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()
    for row in cursor.execute("SELECT * FROM log_data"):
        print(row)
    con.close()
    
    
def flush_database():
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()
    cursor.execute("DROP TABLE IF EXISTS log_data")
    cursor.execute("DROP TABLE IF EXISTS topic_config")
    cursor.execute("DROP TABLE IF EXISTS module_config")
    con.commit()
    con.close()
    setup_database()


OPTIONS = c.ClientOptions(BROKER_URL, name="Broker1")
CLIENT = c.BrokerClient(OPTIONS)

setup_database()
flush_database() # Alleen voor testdoeleinden, verwijder deze regel in productie

CLIENT.CLIENT.on_message = onmessage
CLIENT.CLIENT.subscribe("#")
time.sleep(1)  # Wait for subscription to take effect

CLIENT.publish_message("test/topic", "Hello, MQTT!", retain=True)
CLIENT.publish_message("test/topic", "Yo, MQTT!", retain=True)
# CLIENT.publish_message("test/topic", "Doei, MQTT!", retain=True)
# CLIENT.publish_message("test/topic", "Hello, MQTT!", retain=True)
# CLIENT.publish_message("test/topic", "Hello, MQTT!", retain=True)
# CLIENT.publish_message("test/topic", "Hello, MQTT!", retain=True)
get_messages_from_db()

while True:
    time.sleep(3)
=======

BROKER_URL = "localhost"

OPTIONS = c.ClientOptions(BROKER_URL,name="Broker1")
CLIENT = c.BrokerClient(OPTIONS)

CLIENT.CLIENT.subscribe("#")

while (True):
	time.sleep(3)
>>>>>>> 49a0ee8e8f620b88824b56a15493623f78fbc0b1
