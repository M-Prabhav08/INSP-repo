import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from Module1.Module1 import PacketSnifferGUI
from Module2.Module2 import PacketSender
from Module3.Module3 import NetworkScanner
from Module4.Module4 import VulnerabilityScannerGUI
from Module5.Module5 import RoutingTableGUI
from Module6.Module6 import NetworkMonitorApp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget(self.central_widget)

        self.packet_sniffer_tab = PacketSnifferGUI()
        self.packet_sender_tab = PacketSender()
        self.network_scanner_tab =NetworkScanner()
        self.vulnerability_scanner_tab = VulnerabilityScannerGUI()
        self.RoutingTableGUI=RoutingTableGUI()
        self.NetworkMonitorApp = NetworkMonitorApp()

        self.tab_widget.addTab(self.packet_sniffer_tab, "Packet Sniffer")
        self.tab_widget.addTab(self.packet_sender_tab, "Packet Sender")
        self.tab_widget.addTab(self.network_scanner_tab, "Network Scanner")
        self.tab_widget.addTab(self.vulnerability_scanner_tab, "Vulnerability Scanner")
        self.tab_widget.addTab(self.RoutingTableGUI, "Routing Table")
        self.tab_widget.addTab(self.NetworkMonitorApp, "Network Monitor")

        self.layout.addWidget(self.tab_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
