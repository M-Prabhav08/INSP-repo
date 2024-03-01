import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QFormLayout
from scapy.all import IP, TCP, UDP, ICMP, Ether, send

class PacketSender(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.create_packet_form()

        self.send_button = QPushButton("Send Packet", self.central_widget)
        self.send_button.clicked.connect(self.send_packet)

        self.layout.addWidget(self.send_button)

    def create_packet_form(self):
        form_layout = QFormLayout()

        self.packet_types = ["IP", "TCP", "UDP", "ICMP", "Ethernet"]
        self.packet_type_combo = QComboBox()
        self.packet_type_combo.addItems(self.packet_types)

        self.src_ip_edit = QLineEdit()
        self.dst_ip_edit = QLineEdit()

        self.src_port_edit = QLineEdit()
        self.dst_port_edit = QLineEdit()

        self.data_edit = QLineEdit()

        form_layout.addRow(QLabel("Packet Type:"), self.packet_type_combo)
        form_layout.addRow(QLabel("Source IP:"), self.src_ip_edit)
        form_layout.addRow(QLabel("Destination IP:"), self.dst_ip_edit)
        form_layout.addRow(QLabel("Source Port:"), self.src_port_edit)
        form_layout.addRow(QLabel("Destination Port:"), self.dst_port_edit)
        form_layout.addRow(QLabel("Data:"), self.data_edit)

        self.layout.addLayout(form_layout)

    def send_packet(self):
        packet_type = self.packet_type_combo.currentText()

        if packet_type == "IP":
            packet = IP(src=self.src_ip_edit.text(), dst=self.dst_ip_edit.text())

        elif packet_type == "TCP":
            packet = IP(src=self.src_ip_edit.text(), dst=self.dst_ip_edit.text()) / TCP(sport=int(self.src_port_edit.text()), dport=int(self.dst_port_edit.text()))

        elif packet_type == "UDP":
            packet = IP(src=self.src_ip_edit.text(), dst=self.dst_ip_edit.text()) / UDP(sport=int(self.src_port_edit.text()), dport=int(self.dst_port_edit.text()))

        elif packet_type == "ICMP":
            packet = IP(src=self.src_ip_edit.text(), dst=self.dst_ip_edit.text()) / ICMP()

        elif packet_type == "Ethernet":
            packet = Ether(src=self.src_ip_edit.text(), dst=self.dst_ip_edit.text())

        # Set additional data
        packet = packet / self.data_edit.text()

        # Send the packet
        send(packet)
        print("Packet sent!")

if __name__ == "__main__":
    app = QApplication([])
    window = PacketSender()
    window.show()
    sys.exit(app.exec_())
