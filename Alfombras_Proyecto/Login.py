import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect

from main import Main 



class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setFixedSize(400, 400)  # Tamaño de la ventana de registro

        # Fondo translúcido
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
            }
        """)

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title_label = QLabel("Register")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Campo de Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                height: 30px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.username_input)

        # Campo de Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("""
            QLineEdit {
                height: 30px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.email_input)

        # Campo de Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                height: 30px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.password_input)

        # Botón de Registro
        register_button = QPushButton("Register")
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #6c63ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not email or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        try:
            # Conexión a la base de datos
            connection = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,  # Cambia el puerto si es necesario
                user="root",
                password="",  # Tu contraseña de MariaDB
                database="ventalfombras"
            )
            cursor = connection.cursor()

            # Consulta para insertar al usuario
            query = """
                INSERT INTO vendedores (username, password_hash, email, role)
                VALUES (%s, SHA2(%s, 256), %s, 'vendedor')
            """
            cursor.execute(query, (username, password, email))
            connection.commit()

            QMessageBox.information(self, "Success", "Account created successfully!")
            self.close()  # Cierra la ventana de registro

            # Cerrar conexión
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(800, 600)  # Tamaño fijo de la ventana principal
        self.init_ui()

    def init_ui(self):
        # Ruta de la imagen de fondo
        image_path = r"C:\Users\bglui\OneDrive\Imágenes\fondos2024\backiee-307685.jpg"
        background = QPixmap(image_path).scaled(
            self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        # Configurar el fondo
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palette)

        # Crear contenedor transparente para el login
        self.login_container = QWidget(self)
        self.login_container.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 15px;
            }
        """)

        # Ajustar tamaño y posición inicial del contenedor flotante (centrado)
        container_width = 400
        container_height = 400
        container_x = (self.width() - container_width) // 2
        container_y = (self.height() - container_height) // 2
        self.login_container.setGeometry(container_x, container_y, container_width, container_height)

        login_layout = QVBoxLayout(self.login_container)
        login_layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title_label = QLabel("Login")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(title_label)

        # Campo de Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                height: 30px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        login_layout.addWidget(self.username_input)

        # Campo de Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                height: 30px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        login_layout.addWidget(self.password_input)

        # Botón de Login
        login_button = QPushButton("Login")
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #6c63ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        login_button.clicked.connect(self.authenticate_user)
        login_layout.addWidget(login_button)

        # Texto para registrarse
        register_label = QPushButton("Don't have an account? Register")
        register_label.setFlat(True)
        register_label.setStyleSheet("color: blue; text-decoration: underline;")
        register_label.clicked.connect(self.open_register_window)
        login_layout.addWidget(register_label)

    def authenticate_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        try:
            # Conexión a la base de datos
            connection = mysql.connector.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                password="",
                database="ventalfombras"
            )
            cursor = connection.cursor()

            # Consulta para verificar el usuario
            query = """
                SELECT * FROM vendedores
                WHERE username = %s AND password_hash = SHA2(%s, 256)
            """
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                self.open_main_window()  # Abrir la ventana principal
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

            # Cerrar conexión
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error: {err}")

    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        
    def open_main_window(self):
        self.main_window = Main()
        self.main_window.show()
        self.close()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
