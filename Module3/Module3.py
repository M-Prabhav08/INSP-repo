import sys
from scapy.all import ARP, Ether, srp
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QWidget


class NetworkScanner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.scan_button = QPushButton("Scan Network", self.central_widget)
        self.scan_button.clicked.connect(self.scan_network)

        self.device_table = QTableWidget(self.central_widget)
        self.device_table.setColumnCount(2)  # Columns for IP Address and MAC Address
        self.device_table.setHorizontalHeaderLabels(["IP Address", "MAC Address"])

        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.device_table)

    def scan_network(self):
        result = self.run_arp_scan()

        if result:
            self.display_results(result)

    def run_arp_scan(self):
        try:
            # Get the current machine's IP address and subnet mask
            my_ip, _, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=1), timeout=2, verbose=0)[0][0]

            # Create an ARP request packet for the local network
            target_ip_range = my_ip.split('.')[:-1]  # Get the subnet
            target_ip_range.append("0/24")  # Set the last octet to 0/24 for the local network
            target_ip_range = '.'.join(target_ip_range)

            # Create an ARP request packet
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip_range)

            # Send and receive ARP requests
            result, _ = srp(arp_request, timeout=2, verbose=0)

            # Extract relevant details
            devices = []
            for sent, received in result:
                ip_address = received[ARP].psrc
                mac_address = received[ARP].hwsrc
                devices.append([ip_address, mac_address])

            return devices

        except Exception as e:
            print(f"Error performing ARP scan: {e}")
            return None

    def display_results(self, devices):
        # Clear existing data in the table
        self.device_table.setRowCount(0)

        # Display devices in the table
        for device in devices:
            row_position = self.device_table.rowCount()
            self.device_table.insertRow(row_position)
            for col_position, value in enumerate(device):
                self.device_table.setItem(row_position, col_position, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkScanner()
    window.show()
    sys.exit(app.exec_())
