import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import subprocess

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 800, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.add_title()
        self.add_logo()
        self.add_login_form()

    def add_title(self):
        title_label = QLabel("INTEGRATED NETWORK SECURITY PLATFORM", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(title_label)

    def add_logo(self):
        logo_label = QLabel(self)
        pixmap = QPixmap("./logo.png")  # Replace with the actual path to your logo
        pixmap = pixmap.scaledToWidth(300)  # Resize the logo width as needed
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(logo_label)

    def add_login_form(self):
        login_layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.check_login)

        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_button)

        self.layout.addLayout(login_layout)

    def check_login(self):
    # Replace the following condition with your actual login logic
     if self.username_input.text() == "kiit" and self.password_input.text() == "kiit":
        # If login is successful, run main.py using subprocess in a new process
        import subprocess
        subprocess.Popen(["python", "main.py"])
        self.close()  # Close the LoginWindow after main.py is executed
     else:
        print("Invalid login credentials")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
