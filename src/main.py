import client as c
import time
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

def parse_and_store_metadata(metadata_str):
    # Voorbeeld: "|sensor1|in:topic1,topic2|out:topic3,topic4"
    try:
        parts = metadata_str.strip().split('|')
        # parts[0] is leeg door de leading '|'
        modulenaam = parts[1]
        topics_in = []
        topics_out = []
        for part in parts[2:]:
            if part.startswith("in:"):
                topics_in = [t.strip() for t in part[3:].split(',') if t.strip()]
            elif part.startswith("out:"):
                topics_out = [t.strip() for t in part[4:].split(',') if t.strip()]
    except Exception as e:
        print("Parsing error:", e)
        return

    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()

    # Module toevoegen als die nog niet bestaat
    cursor.execute("SELECT module_id FROM module_config WHERE name_module = ?", (modulenaam,))
    module = cursor.fetchone()
    if not module:
        cursor.execute("INSERT INTO module_config (name_module) VALUES (?)", (modulenaam,))
        con.commit()
        cursor.execute("SELECT module_id FROM module_config WHERE name_module = ?", (modulenaam,))
        module = cursor.fetchone()
    module_id = module[0]

    # Topics toevoegen en koppelen
    for t_in in topics_in:
        cursor.execute("SELECT topic_config_ID FROM topic_config WHERE topic_name = ?", (t_in,))
        t_in_row = cursor.fetchone()
        if not t_in_row:
            cursor.execute("INSERT INTO topic_config (topic_name) VALUES (?)", (t_in,))
            con.commit()
            cursor.execute("SELECT topic_config_ID FROM topic_config WHERE topic_name = ?", (t_in,))
            t_in_row = cursor.fetchone()
        t_in_id = t_in_row[0]
        cursor.execute("INSERT OR IGNORE INTO module_topic_in (module_ID, topic_config_ID) VALUES (?, ?)", (module_id, t_in_id))

    for t_out in topics_out:
        cursor.execute("SELECT topic_config_ID FROM topic_config WHERE topic_name = ?", (t_out,))
        t_out_row = cursor.fetchone()
        if not t_out_row:
            cursor.execute("INSERT INTO topic_config (topic_name) VALUES (?)", (t_out,))
            con.commit()
            cursor.execute("SELECT topic_config_ID FROM topic_config WHERE topic_name = ?", (t_out,))
            t_out_row = cursor.fetchone()
        t_out_id = t_out_row[0]
        cursor.execute("INSERT OR IGNORE INTO module_topic_out (module_ID, topic_config_ID) VALUES (?, ?)", (module_id, t_out_id))

    con.commit()
    con.close()

def log_message_to_log_data(topic, message):
    # Hier kun je eventueel nog parsing doen als je wilt, nu alleen standaard logging
    con = sqlite3.connect(DB_FILE)
    cursor = con.cursor()

    # Topic toevoegen als die nog niet bestaat
    cursor.execute("SELECT topic_config_ID FROM topic_config WHERE topic_name = ?", (topic,))
    topic_row = cursor.fetchone()
    if not topic_row:
        cursor.execute("INSERT INTO topic_config (topic_name) VALUES (?)", (topic,))
        con.commit()
        topic_config_id = cursor.lastrowid
    else:
        topic_config_id = topic_row[0]

    # Log het bericht
    cursor.execute(
        "INSERT INTO log_data (message, topic_config_ID, date_logged) VALUES (?, ?, datetime('now', '+2 hours'))",
        (message, topic_config_id)
    )
    con.commit()
    con.close()

def onmessage(client, userdata, message):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")
    if message.topic == "metadata":
        parse_and_store_metadata(message.payload.decode())
    else:
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
    cursor.execute("DROP TABLE IF EXISTS module_topic_in")
    cursor.execute("DROP TABLE IF EXISTS module_topic_out")
    con.commit()
    con.close()
    setup_database()

OPTIONS = c.ClientOptions(BROKER_URL, name="Broker1")
CLIENT = c.BrokerClient(OPTIONS)

setup_database()
# flush_database() # Alleen voor testdoeleinden, verwijder deze regel in productie

CLIENT.CLIENT.on_message = onmessage
CLIENT.CLIENT.subscribe("#")
time.sleep(1)  # Wachten tot de client is verbonden en klaar is met subscriben

# Voorbeeld: stuur metadata-bericht (in praktijk gebeurt dit via MQTT publish)
CLIENT.publish_message("metadata", "|sensor1|in:test/topic,other/in|out:result/topic", retain=True)

CLIENT.publish_message("test/topic", "Hello, MQTT!", retain=True)
CLIENT.publish_message("test/topic", "Yo, MQTT!", retain=True)
get_messages_from_db()

while True:
    time.sleep(3)