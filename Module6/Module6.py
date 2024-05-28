import sys
import time
import threading
from collections import defaultdict
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def capture_packet():
   
    return ("192.168.1.100", "8.8.8.8", "HTTP", 1500)


class NetworkMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network Monitor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

       
        self.bandwidth_figure = Figure()
        self.bandwidth_canvas = FigureCanvas(self.bandwidth_figure)
        self.layout.addWidget(self.bandwidth_canvas)

        
        self.protocol_figure = Figure()
        self.protocol_canvas = FigureCanvas(self.protocol_figure)
        self.layout.addWidget(self.protocol_canvas)

        
        self.bandwidth_data = defaultdict(int)
        self.protocol_data = defaultdict(int)

        
        self.monitor_thread = threading.Thread(target=self.monitor_network)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

 
    def update_plots(self):
        while True:
            
            source_ip, destination_ip, protocol, payload_size = capture_packet()

            
            self.bandwidth_data[protocol] += payload_size

            
            self.protocol_data[protocol] += 1

            self.update_bandwidth_plot()

           
            self.update_protocol_plot()

            time.sleep(1)  

    def update_bandwidth_plot(self):
        self.bandwidth_figure.clear()
        ax = self.bandwidth_figure.add_subplot(111)
        ax.bar(self.bandwidth_data.keys(), self.bandwidth_data.values())
        ax.set_title('Bandwidth Usage')
        ax.set_xlabel('Protocol')
        ax.set_ylabel('Data (bytes)')
        ax.set_xticklabels(self.bandwidth_data.keys(), rotation=45)
        self.bandwidth_canvas.draw()

   
    def update_protocol_plot(self):
        self.protocol_figure.clear()
        ax = self.protocol_figure.add_subplot(111)
        ax.pie(self.protocol_data.values(), labels=self.protocol_data.keys(), autopct='%1.1f%%')
        ax.set_title('Protocol Distribution')
        self.protocol_canvas.draw()

   
    def monitor_network(self):
        self.update_plots()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkMonitorApp()
    window.show()
    sys.exit(app.exec_())
