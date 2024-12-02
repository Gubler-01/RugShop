import sys
import mysql.connector
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QMessageBox, QDialog, 
    QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView
)

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Cambia según tu configuración
        database="ventalfombras"
    )

### --- DIÁLOGOS PARA CLIENTES --- ###
class AgregarClienteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Cliente")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5DC;
                border-radius: 15px;
            }
            QLabel {
                font-size: 14px;
                color: #2C3E50;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #2C3E50;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)

        layout = QFormLayout()

        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.email_input = QLineEdit()

        guardar_btn = QPushButton("Guardar")
        guardar_btn.clicked.connect(self.guardar_cliente)

        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Teléfono:", self.telefono_input)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("Correo:", self.email_input)
        layout.addRow(guardar_btn)

        self.setLayout(layout)

    def guardar_cliente(self):
        nombre = self.nombre_input.text()
        telefono = self.telefono_input.text()
        direccion = self.direccion_input.text()
        email = self.email_input.text()

        if not nombre or not telefono or not direccion or not email:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombre, telefono, direccion, correo) 
                VALUES (%s, %s, %s, %s)
            """, (nombre, telefono, direccion, email))
            conn.commit()
            QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al agregar cliente: {e}")
        finally:
            cursor.close()
            conn.close()

class ListarClientesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Listar Clientes")
        self.setGeometry(200, 200, 800, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #FAF3E0;
                border-radius: 15px;
            }
            QLabel {
                font-size: 16px;
                color: #34495E;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #ECF0F1;
                border: 2px solid #34495E;
                border-radius: 10px;
                font-size: 14px;
                gridline-color: #95A5A6;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #1ABC9C;
                color: white;
                font-size: 14px;
                padding: 5px;
                border: none;
            }
        """)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Teléfono", "Correo"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.cargar_clientes()

    def cargar_clientes(self):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, telefono, correo FROM clientes")
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar clientes: {e}")
        finally:
            cursor.close()
            conn.close()

### --- DIÁLOGOS PARA VENDEDORES --- ###
class AgregarVendedorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Vendedor")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5DC;
                border-radius: 15px;
            }
            QLabel {
                font-size: 14px;
                color: #2C3E50;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #2C3E50;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
        """)

        layout = QFormLayout()

        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        guardar_btn = QPushButton("Guardar")
        guardar_btn.clicked.connect(self.guardar_vendedor)

        layout.addRow("Username:", self.username_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow(guardar_btn)

        self.setLayout(layout)

    def guardar_vendedor(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vendedores (username, password_hash, email, role) 
                VALUES (%s, SHA2(%s, 256), %s, 'vendedor')
            """, (username, password, email))
            conn.commit()
            QMessageBox.information(self, "Éxito", "Vendedor agregado correctamente.")
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al agregar vendedor: {e}")
        finally:
            cursor.close()
            conn.close()

class ListarVendedoresDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Listar Vendedores")
        self.setGeometry(200, 200, 800, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #FAF3E0;
                border-radius: 15px;
            }
            QLabel {
                font-size: 16px;
                color: #34495E;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #ECF0F1;
                border: 2px solid #34495E;
                border-radius: 10px;
                font-size: 14px;
                gridline-color: #95A5A6;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #1ABC9C;
                color: white;
                font-size: 14px;
                padding: 5px;
                border: none;
            }
        """)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Email", "Rol"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.cargar_vendedores()

    def cargar_vendedores(self):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, role FROM vendedores")
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar vendedores: {e}")
        finally:
            cursor.close()
            conn.close()

### --- VENTANA PRINCIPAL --- ###
class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🌟 Sistema de Venta de Alfombras 🌟")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QLabel {
                font-size: 24px;
                color: #2E4053;
                font-weight: bold;
                margin: 20px;
            }
        """)

        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: #34495E; color: white; font-size: 14px;")

        # Menú de Clientes
        clientes_menu = menu_bar.addMenu("Clientes")
        agregar_cliente_action = QAction("Agregar Cliente", self)
        listar_clientes_action = QAction("Listar Clientes", self)
        clientes_menu.addAction(agregar_cliente_action)
        clientes_menu.addAction(listar_clientes_action)
        agregar_cliente_action.triggered.connect(self.agregar_cliente)
        listar_clientes_action.triggered.connect(self.listar_clientes)

        # Menú de Vendedores
        vendedores_menu = menu_bar.addMenu("Usuarios")
        agregar_vendedor_action = QAction("Agregar Vendedor", self)
        listar_vendedores_action = QAction("Listar Vendedores", self)
        vendedores_menu.addAction(agregar_vendedor_action)
        vendedores_menu.addAction(listar_vendedores_action)
        agregar_vendedor_action.triggered.connect(self.agregar_vendedor)
        listar_vendedores_action.triggered.connect(self.listar_vendedores)

        welcome_label = QLabel("🌟 Bienvenido al Sistema de Venta de Alfombras 🌟")
        welcome_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(welcome_label)

    def agregar_cliente(self):
        dialog = AgregarClienteDialog(self)
        dialog.exec_()

    def listar_clientes(self):
        dialog = ListarClientesDialog(self)
        dialog.exec_()

    def agregar_vendedor(self):
        dialog = AgregarVendedorDialog(self)
        dialog.exec_()

    def listar_vendedores(self):
        dialog = ListarVendedoresDialog(self)
        dialog.exec_()

### --- EJECUCIÓN --- ###
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
