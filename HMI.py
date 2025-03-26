import sys
import socket
import json
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDateTimeEdit
from datetime import datetime
from influxdb import InfluxDBClient

# Configuration
CONTROLLER_IP = "192.168.1.100"  # Update with actual IP
CONTROLLER_PORT = 5000  # Update if needed
INFLUXDB_HOST = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = "hmi_data"


class HMI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HMI Interface")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()
        self.influx_client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
        self.influx_client.switch_database(INFLUXDB_DATABASE)

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Select Time Period:")
        layout.addWidget(self.label)

        self.start_time = QDateTimeEdit(self)
        self.start_time.setDateTime(datetime.now())
        layout.addWidget(self.start_time)

        self.end_time = QDateTimeEdit(self)
        self.end_time.setDateTime(datetime.now())
        layout.addWidget(self.end_time)

        self.fetch_button = QPushButton("Fetch Data", self)
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def fetch_data(self):
        start_timestamp = self.start_time.dateTime().toSecsSinceEpoch()
        end_timestamp = self.end_time.dateTime().toSecsSinceEpoch()

        request_data = json.dumps({"command": "get_data", "start": start_timestamp, "end": end_timestamp})

        try:
            with socket.create_connection((CONTROLLER_IP, CONTROLLER_PORT), timeout=5) as s:
                s.sendall(request_data.encode())
                response = s.recv(4096)
                data = json.loads(response.decode())
                self.store_data_in_influx(data)
        except Exception as e:
            self.label.setText(f"Error: {e}")

    def store_data_in_influx(self, data):
        points = []
        for entry in data:
            points.append({
                "measurement": "sensor_data",
                "time": entry["timestamp"],
                "fields": {"value": entry["value"]}
            })
        self.influx_client.write_points(points)
        self.label.setText("Data stored successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HMI()
    window.show()
    sys.exit(app.exec_())
