import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import nmap


class VulnerabilityScannerGUI(QMainWindow):
    def __init__(self):
        super(VulnerabilityScannerGUI, self).__init__()

        self.setWindowTitle("Vulnerability Scanner")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

       
        self.target_ip_input = QLineEdit(self)
        self.target_ip_input.setPlaceholderText("Enter Target IP")
        self.layout.addWidget(self.target_ip_input)

        self.start_button = QPushButton("Start Scan", self)
        self.start_button.clicked.connect(self.start_scan)
        self.layout.addWidget(self.start_button)

       
        self.stop_button = QPushButton("Stop Scan", self)
        self.stop_button.clicked.connect(self.stop_scan)
        self.layout.addWidget(self.stop_button)

       
        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(["Port", "Service", "Vulnerabilities"])
        self.layout.addWidget(self.result_table)

        self.central_widget.setLayout(self.layout)

        
        self.scanner = VulnerabilityScanner()

    def start_scan(self):
        target_ip = self.target_ip_input.text()
        if target_ip:
            self.result_table.setRowCount(0)  

            scan_result = self.scanner.scan_target(target_ip)
            if scan_result:
                for port, service, vulnerabilities in scan_result:
                    self.add_result_to_table(port, service, vulnerabilities)

    def stop_scan(self):
        
        pass

    def add_result_to_table(self, port, service, vulnerabilities):
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        self.result_table.setItem(row_position, 0, QTableWidgetItem(str(port)))
        self.result_table.setItem(row_position, 1, QTableWidgetItem(service))
        self.result_table.setItem(row_position, 2, QTableWidgetItem(vulnerabilities))


class VulnerabilityScanner:
    def __init__(self):
        self.nm = nmap.PortScanner(nmap_search_path=('C:\\Program Files (x86)\\Nmap\\nmap.exe',))

    def scan_target(self, target_ip):
        try:
            self.nm.scan(hosts=target_ip, arguments='-sV --script vuln')
            scan_data = []

            for host in self.nm.all_hosts():
                for proto in self.nm[host].all_protocols():
                    lport = self.nm[host][proto].keys()
                    for port in lport:
                        service = self.nm[host][proto][port]['name']
                        script_output = self.nm[host][proto][port].get('script', {})
                        vulnerabilities = "; ".join(script_output.values()) if script_output else "None"
                        scan_data.append((port, service, vulnerabilities))

            return scan_data

        except nmap.PortScannerError as e:
            print(f"nmap Error: {e}")
            return None

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VulnerabilityScannerGUI()
    window.show()
    sys.exit(app.exec_())
