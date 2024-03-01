import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        self.setWindowTitle("Login")
        self.setMinimumSize(600, 300)  # Set a minimum size for the window

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout for the central widget
        self.layout = QVBoxLayout(self.central_widget)

        # Add the login title
        self.add_login_title()

        # Add a spacer item to create some space between the title and the login form
        spacer_item = QWidget(self)
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(spacer_item)

        # Add the login form with logo
        self.add_login_form()

    def add_login_title(self):
        login_title_label = QLabel("Login", self)
        login_title_label.setAlignment(Qt.AlignCenter)
        login_title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.layout.addWidget(login_title_label)

    def add_login_form(self):
        login_layout = QHBoxLayout()

        # Create a widget to contain the login layout and set its style sheet
        login_widget = QWidget(self)
        login_widget.setStyleSheet("""
            background-color: #f0f0f0;
            border: 1px solid #d0d0d0;
            border-radius: 10px;
            padding: 20px;
            margin: 20px;
        """)

        # Add the logo image to the login widget
        logo_label = QLabel(self)
        pixmap = QPixmap("./logo.png")  # Replace with the actual path to your logo
        pixmap = pixmap.scaledToWidth(330)  # Resize the logo width as needed
        logo_label.setPixmap(pixmap)
        login_layout.addWidget(logo_label)

        # Add the login input fields and button
        login_input_layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("User Name")
        self.username_input.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0);
            border: none;
            border-bottom: 2px solid rgba(46, 82, 101, 200);
            color: rgba(0, 0, 0, 240);
            padding-bottom: 7px;
        """)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0);
            border: none;
            border-bottom: 2px solid rgba(46, 82, 101, 200);
            color: rgba(0, 0, 0, 240);
            padding-bottom: 7px;
        """)

        login_button = QPushButton("Log In", self)
        login_button.clicked.connect(self.check_login)
        login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4D90FE, stop: 1 #306EFF);
                border-radius: 5px;
                color: white;
            }

            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4D90FE, stop: 1 #3E6FD4);
            }

            QPushButton:pressed {
                padding-left: 5px;
                padding-top: 5px;
                background-color: rgba(150, 123, 111, 255);
            }
        """)

        login_input_layout.addWidget(self.username_input)
        login_input_layout.addWidget(self.password_input)
        login_input_layout.addWidget(login_button)

        # Set the layout for the login input fields and button
        login_widget.setLayout(login_input_layout)

        # Add the login widget to the main layout
        login_layout.addWidget(login_widget)

        # Set the layout for the central widget
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
