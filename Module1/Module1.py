from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit, QWidget
from PyQt5.QtCore import QTimer
from scapy.all import sniff, IP, TCP, UDP
import sys

class PacketSnifferGUI(QMainWindow):
    def __init__(self):
        super(PacketSnifferGUI, self).__init__()

        self.setWindowTitle("Packet Sniffer & Analysis Toolkit")
        self.setGeometry(100, 100, 1200, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.capture_button = QPushButton("Start Capture", self)
        self.capture_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.capture_button)

        self.stop_button = QPushButton("Stop Capture", self)
        self.stop_button.clicked.connect(self.stop_capture)
        self.layout.addWidget(self.stop_button)

        self.packet_table = QTableWidget(self)
        self.packet_table.setColumnCount(11)
        self.packet_table.setHorizontalHeaderLabels(["Time", "Source", "Destination", "Source Port", "Destination Port", "Protocol", "Length", "TTL", "Flags", "Info", "Data"])
        self.layout.addWidget(self.packet_table)

        self.central_widget.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)

        self.packets = []

    def start_capture(self):
        self.packet_table.setRowCount(0)
        self.packets = []
        self.timer.start(1000)  

    def stop_capture(self):
        self.timer.stop()

    def update_table(self):
        new_packets = sniff(count=10, timeout=1)  

        for packet in new_packets:
            self.packets.append(packet)
            self.add_packet_to_table(packet)

    def add_packet_to_table(self, packet):
        row_position = self.packet_table.rowCount()
        self.packet_table.insertRow(row_position)

        time = packet.time
        source = packet[IP].src if IP in packet else "N/A"
        destination = packet[IP].dst if IP in packet else "N/A"
        source_port = packet.sport if TCP in packet or UDP in packet else "N/A"
        destination_port = packet.dport if TCP in packet or UDP in packet else "N/A"
        protocol = packet[IP].proto if IP in packet else "N/A"
        length = len(packet)
        ttl = packet[IP].ttl if IP in packet else "N/A"
        flags = packet[TCP].flags if TCP in packet else "N/A"
        info = packet.summary()
        data = str(packet)

        self.packet_table.setItem(row_position, 0, QTableWidgetItem(str(time)))
        self.packet_table.setItem(row_position, 1, QTableWidgetItem(source))
        self.packet_table.setItem(row_position, 2, QTableWidgetItem(destination))
        self.packet_table.setItem(row_position, 3, QTableWidgetItem(str(source_port)))
        self.packet_table.setItem(row_position, 4, QTableWidgetItem(str(destination_port)))
        self.packet_table.setItem(row_position, 5, QTableWidgetItem(str(protocol)))
        self.packet_table.setItem(row_position, 6, QTableWidgetItem(str(length)))
        self.packet_table.setItem(row_position, 7, QTableWidgetItem(str(ttl)))
        self.packet_table.setItem(row_position, 8, QTableWidgetItem(str(flags)))
        self.packet_table.setItem(row_position, 9, QTableWidgetItem(info))
        self.packet_table.setItem(row_position, 10, QTableWidgetItem(data))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PacketSnifferGUI()
    window.show()
    sys.exit(app.exec_())
