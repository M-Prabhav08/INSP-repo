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

        
        self.capture_button = QPushButton("Start Capture", self)  
        self.capture_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.capture_button)

        
        self.packet_table = QTableWidget(self)
        self.packet_table.setColumnCount(4)
        self.packet_table.setHorizontalHeaderLabels(["Source", "Destination", "Protocol", "Data"])
        self.layout.addWidget(self.packet_table)

        

        self.central_widget.setLayout(self.layout)

    def start_capture(self):
        
        self.packet_table.setRowCount(0)

        
        packets = sniff(count=20) 

        
        for packet in packets:
            self.add_packet_to_table(packet)

    def add_packet_to_table(self, packet):
        row_position = self.packet_table.rowCount()
        self.packet_table.insertRow(row_position)

        
        source = packet[IP].src
        destination = packet[IP].dst
        protocol = packet[IP].proto
        data = str(packet.summary())

        
        self.packet_table.setItem(row_position, 0, QTableWidgetItem(source))
        self.packet_table.setItem(row_position, 1, QTableWidgetItem(destination))
        self.packet_table.setItem(row_position, 2, QTableWidgetItem(str(protocol)))
        self.packet_table.setItem(row_position, 3, QTableWidgetItem(data))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PacketSnifferGUI()
    window.show()
    sys.exit(app.exec_())
