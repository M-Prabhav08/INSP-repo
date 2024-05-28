import sys
from scapy.all import ARP, Ether, srp, conf, get_if_addr, getmacbyip
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
        self.device_table.setColumnCount(4) 
        self.device_table.setHorizontalHeaderLabels(["IP Address", "MAC Address"])

        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.device_table)

    def scan_network(self):
        result = self.run_arp_scan()

        if result:
            self.display_results(result)

    def run_arp_scan(self):
        try:
           
            src_ip = get_if_addr(conf.iface)
            ip_parts = src_ip.split('.')
            target_ip_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"

            
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip_range)

           
            result, _ = srp(arp_request, timeout=2, verbose=0)

            
            devices = []
            for sent, received in result:
                ip_address = received.psrc
                mac_address = received.hwsrc


                devices.append([ip_address, mac_address])

            return devices

        except Exception as e:
            print(f"Error performing ARP scan: {e}")
            return None

    def display_results(self, devices):
        
        self.device_table.setRowCount(0)

        
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
