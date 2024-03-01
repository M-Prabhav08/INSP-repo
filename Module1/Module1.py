from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QLineEdit, QWidget
from scapy.all import sniff
from scapy.all import sniff, IP 
import sys

class PacketSnifferGUI(QMainWindow):
    def __init__(self):
        super(PacketSnifferGUI, self).__init__()

        self.setWindowTitle("Packet Sniffer & Analysis Toolkit")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Capture Button
        self.capture_button = QPushButton("Start Capture", self)
        self.capture_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.capture_button)

        # Table Display
        self.packet_table = QTableWidget(self)
        self.packet_table.setColumnCount(4)
        self.packet_table.setHorizontalHeaderLabels(["Source", "Destination", "Protocol", "Data"])
        self.layout.addWidget(self.packet_table)

        # Search Box
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self.filter_packets)
        self.layout.addWidget(self.search_box)

        self.central_widget.setLayout(self.layout)

    def start_capture(self):
        # Clear existing table content
        self.packet_table.setRowCount(0)

        # Sniff packets
        packets = sniff(count=20)  # Capture 10 packets for demonstration

        # Update the table
        for packet in packets:
            self.add_packet_to_table(packet)

    def add_packet_to_table(self, packet):
        row_position = self.packet_table.rowCount()
        self.packet_table.insertRow(row_position)

        # Extract relevant information from the packet
        source = packet[IP].src
        destination = packet[IP].dst
        protocol = packet[IP].proto
        data = str(packet.summary())

        # Populate the table with packet information
        self.packet_table.setItem(row_position, 0, QTableWidgetItem(source))
        self.packet_table.setItem(row_position, 1, QTableWidgetItem(destination))
        self.packet_table.setItem(row_position, 2, QTableWidgetItem(str(protocol)))
        self.packet_table.setItem(row_position, 3, QTableWidgetItem(data))

    def filter_packets(self, text):
        # TODO: Implement packet filtering based on the search text
        for row in range(self.packet_table.rowCount()):
            for col in range(self.packet_table.columnCount()):
                item = self.packet_table.item(row, col)
                if text.lower() in item.text().lower():
                    self.packet_table.setRowHidden(row, False)
                    break
                else:
                    self.packet_table.setRowHidden(row, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PacketSnifferGUI()
    window.show()
    sys.exit(app.exec_())
