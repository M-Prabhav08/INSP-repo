import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QFormLayout, QTextEdit
from PyQt5.QtCore import pyqtSignal, QThread
from scapy.all import IP, TCP, UDP, ICMP, Ether, send, get_if_addr, conf

class PacketSenderThread(QThread):
    packet_sent_signal = pyqtSignal(str)

    def __init__(self, packet_type, dst_ip, src_port, dst_port, data, src_ip):
        super().__init__()
        self.packet_type = packet_type
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.data = data
        self.src_ip = src_ip
        self.running = True

    def run(self):
        while self.running:
            if self.packet_type == "IP":
                packet = IP(src=self.src_ip, dst=self.dst_ip)
            elif self.packet_type == "TCP":
                packet = IP(src=self.src_ip, dst=self.dst_ip) / TCP(sport=int(self.src_port), dport=int(self.dst_port))
            elif self.packet_type == "UDP":
                packet = IP(src=self.src_ip, dst=self.dst_ip) / UDP(sport=int(self.src_port), dport=int(self.dst_port))
            elif self.packet_type == "ICMP":
                packet = IP(src=self.src_ip, dst=self.dst_ip) / ICMP()
            elif self.packet_type == "Ethernet":
                packet = Ether(src=self.src_ip, dst=self.dst_ip)

            packet = packet / self.data
            send(packet, verbose=False)
            self.packet_sent_signal.emit("Packet sent!")

    def stop(self):
        self.running = False

class PacketSender(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.create_packet_form()

        self.send_button = QPushButton("Send Packet", self.central_widget)
        self.send_button.clicked.connect(self.start_sending_packets)
        self.layout.addWidget(self.send_button)

        self.stop_button = QPushButton("Stop", self.central_widget)
        self.stop_button.clicked.connect(self.stop_sending_packets)
        self.layout.addWidget(self.stop_button)

        self.log_text = QTextEdit(self.central_widget)
        self.log_text.setReadOnly(True)
        self.layout.addWidget(self.log_text)

        self.packet_sender_thread = None

    def create_packet_form(self):
        form_layout = QFormLayout()

        self.packet_types = ["IP", "TCP", "UDP", "ICMP", "Ethernet"]
        self.packet_type_combo = QComboBox()
        self.packet_type_combo.addItems(self.packet_types)

        self.dst_ip_edit = QLineEdit()
        self.src_port_edit = QLineEdit()
        self.dst_port_edit = QLineEdit()
        self.data_edit = QLineEdit()

        form_layout.addRow(QLabel("Packet Type:"), self.packet_type_combo)
        form_layout.addRow(QLabel("Destination IP:"), self.dst_ip_edit)
        form_layout.addRow(QLabel("Source Port:"), self.src_port_edit)
        form_layout.addRow(QLabel("Destination Port:"), self.dst_port_edit)
        form_layout.addRow(QLabel("Data:"), self.data_edit)

        self.layout.addLayout(form_layout)

    def start_sending_packets(self):
        src_ip = get_if_addr(conf.iface)
        dst_ip = self.dst_ip_edit.text()
        src_port = self.src_port_edit.text()
        dst_port = self.dst_port_edit.text()
        data = self.data_edit.text()
        packet_type = self.packet_type_combo.currentText()

        self.packet_sender_thread = PacketSenderThread(packet_type, dst_ip, src_port, dst_port, data, src_ip)
        self.packet_sender_thread.packet_sent_signal.connect(self.log_packet_sent)
        self.packet_sender_thread.start()

    def stop_sending_packets(self):
        if self.packet_sender_thread:
            self.packet_sender_thread.stop()
            self.packet_sender_thread = None

    def log_packet_sent(self, message):
        self.log_text.append(message)

if __name__ == "__main__":
    app = QApplication([])
    window = PacketSender()
    window.show()
    sys.exit(app.exec_())
