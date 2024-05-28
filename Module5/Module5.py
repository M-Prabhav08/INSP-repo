import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class RoutingTableGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Routing Table")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Destination", "Gateway", "Genmask", "Flags"])
        self.layout.addWidget(self.result_table)

        self.central_widget.setLayout(self.layout)

        self.display_routing_table()

    def display_routing_table(self):
        routing_table_output = self.get_routing_table()
        if routing_table_output:
            self.populate_table(routing_table_output)

    def get_routing_table(self):
        try:
            result = subprocess.run(['netstat', '-rn'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.splitlines()
            else:
                print("Error: Failed to fetch routing table.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def populate_table(self, routing_table_output):
        self.result_table.setRowCount(0)

        for line in routing_table_output[3:]: 
            data = line.split()
            if len(data) >= 5:  
                destination = data[0]
                gateway = data[2]
                genmask = data[3]
                flags = data[4]
                self.add_row_to_table(destination, gateway, genmask, flags)

    def add_row_to_table(self, destination, gateway, genmask, flags):
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        self.result_table.setItem(row_position, 0, QTableWidgetItem(destination))
        self.result_table.setItem(row_position, 1, QTableWidgetItem(gateway))
        self.result_table.setItem(row_position, 2, QTableWidgetItem(genmask))
        self.result_table.setItem(row_position, 3, QTableWidgetItem(flags))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoutingTableGUI()
    window.show()
    sys.exit(app.exec_())
