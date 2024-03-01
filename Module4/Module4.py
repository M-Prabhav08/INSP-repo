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

        # Target IP Input
        self.target_ip_input = QLineEdit(self)
        self.target_ip_input.setPlaceholderText("Enter Target IP")
        self.layout.addWidget(self.target_ip_input)

        # Start Button
        self.start_button = QPushButton("Start Scan", self)
        self.start_button.clicked.connect(self.start_scan)
        self.layout.addWidget(self.start_button)

        # Stop Button
        self.stop_button = QPushButton("Stop Scan", self)
        self.stop_button.clicked.connect(self.stop_scan)
        self.layout.addWidget(self.stop_button)

        # Result Table
        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Port", "Service"])
        self.layout.addWidget(self.result_table)

        self.central_widget.setLayout(self.layout)

        # Scanner initialization
        self.scanner = VulnerabilityScanner()

    def start_scan(self):
        target_ip = self.target_ip_input.text()
        if target_ip:
            self.result_table.setRowCount(0)  # Clear existing rows

            scan_result = self.scanner.scan_target(target_ip)
            if scan_result:
                for port, service in scan_result.items():
                    self.add_result_to_table(port, service)

    def stop_scan(self):
        # Implement logic to stop the scan if needed
        pass

    def add_result_to_table(self, port, service):
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        self.result_table.setItem(row_position, 0, QTableWidgetItem(str(port)))
        self.result_table.setItem(row_position, 1, QTableWidgetItem(service))

class VulnerabilityScanner:
    def __init__(self):
        self.nm = nmap.PortScanner(nmap_search_path=('C:\\Program Files (x86)\\Nmap\\nmap.exe',))

    def scan_target(self, target_ip):
        try:
            self.nm.scan(hosts=target_ip, arguments='-sV')
            return self.nm[target_ip]

        except nmap.PortScannerError as e:
            print(f"nmap Error: {e}")
            return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VulnerabilityScannerGUI()
    window.show()
    sys.exit(app.exec_())
