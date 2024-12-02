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

### --- DIÁLOGOS PARA PRODUCTOS --- ###
class AgregarProductoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Producto")
        self.setGeometry(300, 300, 400, 350)
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
            QLineEdit, QTextEdit {
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

        self.codigo_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.descripcion_input = QLineEdit()
        self.precio_input = QLineEdit()
        self.stock_input = QLineEdit()

        guardar_btn = QPushButton("Guardar Producto")
        guardar_btn.clicked.connect(self.guardar_producto)

        layout.addRow("Código Producto:", self.codigo_input)
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Descripción:", self.descripcion_input)
        layout.addRow("Precio:", self.precio_input)
        layout.addRow("Stock:", self.stock_input)
        layout.addRow(guardar_btn)

        self.setLayout(layout)

    def guardar_producto(self):
        codigo_producto = self.codigo_input.text()
        nombre = self.nombre_input.text()
        descripcion = self.descripcion_input.text()
        precio = self.precio_input.text()
        stock = self.stock_input.text()

        if not codigo_producto or not nombre or not precio or not stock:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            precio = float(precio)
            stock = int(stock)
        except ValueError:
            QMessageBox.warning(self, "Error", "Precio y Stock deben ser numéricos.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO productos (codigo_producto, nombre, descripcion, precio, stock) 
                VALUES (%s, %s, %s, %s, %s)
            """, (codigo_producto, nombre, descripcion, precio, stock))
            conn.commit()
            QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al agregar producto: {e}")
        finally:
            cursor.close()
            conn.close()

class ListarProductosDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Listar Productos")
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Código", "Nombre", "Descripción", "Precio", "Stock"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.cargar_productos()

    def cargar_productos(self):
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, codigo_producto, nombre, descripcion, precio, stock FROM productos"
            )
            rows = cursor.fetchall()

            self.table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar productos: {e}")
        finally:
            cursor.close()
            conn.close()

class ActualizarProductoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Actualizar Producto")
        self.setGeometry(300, 300, 400, 350)
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
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
                width: 100%;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
            QFormLayout {
                spacing: 15px;
                margin: 15px;
            }
        """)

        layout = QFormLayout()

        self.id_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.descripcion_input = QLineEdit()
        self.precio_input = QLineEdit()
        self.stock_input = QLineEdit()

        buscar_btn = QPushButton("Buscar Producto")
        buscar_btn.clicked.connect(self.buscar_producto)

        actualizar_btn = QPushButton("Actualizar Producto")
        actualizar_btn.clicked.connect(self.actualizar_producto)

        layout.addRow("ID Producto:", self.id_input)
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Descripción:", self.descripcion_input)
        layout.addRow("Precio:", self.precio_input)
        layout.addRow("Stock:", self.stock_input)
        layout.addRow(buscar_btn)
        layout.addRow(actualizar_btn)

        self.setLayout(layout)

    def buscar_producto(self):
        producto_id = self.id_input.text()
        if not producto_id:
            QMessageBox.warning(self, "Error", "El ID del producto es obligatorio.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nombre, descripcion, precio, stock FROM productos WHERE id = %s",
                (producto_id,),
            )
            producto = cursor.fetchone()
            if producto:
                self.nombre_input.setText(producto[0])
                self.descripcion_input.setText(producto[1])
                self.precio_input.setText(str(producto[2]))
                self.stock_input.setText(str(producto[3]))
            else:
                QMessageBox.warning(self, "Error", "Producto no encontrado.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al buscar producto: {e}")
        finally:
            cursor.close()
            conn.close()

    def actualizar_producto(self):
        producto_id = self.id_input.text()
        nombre = self.nombre_input.text()
        descripcion = self.descripcion_input.text()
        precio = self.precio_input.text()
        stock = self.stock_input.text()

        if not producto_id or not nombre or not precio or not stock:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos
                SET nombre = %s, descripcion = %s, precio = %s, stock = %s
                WHERE id = %s
            """, (nombre, descripcion, precio, stock, producto_id))
            conn.commit()
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente.")
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar producto: {e}")
        finally:
            cursor.close()
            conn.close()


class EliminarProductoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Producto")
        self.setGeometry(300, 300, 400, 200)
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
                background-color: #E74C3C;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)

        layout = QFormLayout()

        self.id_input = QLineEdit()
        eliminar_btn = QPushButton("Eliminar Producto")
        eliminar_btn.clicked.connect(self.eliminar_producto)

        layout.addRow("ID Producto:", self.id_input)
        layout.addRow(eliminar_btn)

        self.setLayout(layout)

    def eliminar_producto(self):
        producto_id = self.id_input.text()
        if not producto_id:
            QMessageBox.warning(self, "Error", "El ID del producto es obligatorio.")
            return

        # Confirmar la eliminación
        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el producto con ID {producto_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            try:
                # Conectar a la base de datos
                conn = conectar_db()
                cursor = conn.cursor()
                
                # Eliminar el producto de la base de datos
                cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
                
                # Confirmar cambios
                conn.commit()

                # Mostrar mensaje de éxito
                QMessageBox.information(self, "Éxito", f"Producto con ID {producto_id} eliminado correctamente.")
                
                # Cerrar la ventana
                self.close()

            except mysql.connector.Error as e:
                # Mostrar error en caso de fallo
                QMessageBox.critical(self, "Error", f"Error al eliminar producto: {e}")
            finally:
                # Cerrar la conexión
                cursor.close()
                conn.close()


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

class ActualizarClienteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Actualizar Cliente")
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

        self.id_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.direccion_input = QLineEdit()
        self.email_input = QLineEdit()

        buscar_btn = QPushButton("Buscar Cliente")
        buscar_btn.clicked.connect(self.buscar_cliente)

        guardar_btn = QPushButton("Actualizar Cliente")
        guardar_btn.clicked.connect(self.actualizar_cliente)

        layout.addRow("ID Cliente:", self.id_input)
        layout.addRow("Nombre:", self.nombre_input)
        layout.addRow("Teléfono:", self.telefono_input)
        layout.addRow("Dirección:", self.direccion_input)
        layout.addRow("Correo:", self.email_input)
        layout.addRow(buscar_btn)
        layout.addRow(guardar_btn)

        self.setLayout(layout)

    def buscar_cliente(self):
        cliente_id = self.id_input.text()
        if not cliente_id:
            QMessageBox.warning(self, "Error", "El ID del cliente es obligatorio.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, telefono, direccion, correo FROM clientes WHERE id = %s", (cliente_id,))
            cliente = cursor.fetchone()

            if cliente:
                self.nombre_input.setText(cliente[0])
                self.telefono_input.setText(cliente[1])
                self.direccion_input.setText(cliente[2])
                self.email_input.setText(cliente[3])
            else:
                QMessageBox.warning(self, "Error", "Cliente no encontrado.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al buscar cliente: {e}")
        finally:
            cursor.close()
            conn.close()

    def actualizar_cliente(self):
        cliente_id = self.id_input.text()
        nombre = self.nombre_input.text()
        telefono = self.telefono_input.text()
        direccion = self.direccion_input.text()
        email = self.email_input.text()

        if not all([cliente_id, nombre, telefono, direccion, email]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nombre = %s, telefono = %s, direccion = %s, correo = %s
                WHERE id = %s
            """, (nombre, telefono, direccion, email, cliente_id))
            conn.commit()
            QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente.")
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar cliente: {e}")
        finally:
            cursor.close()
            conn.close()


class EliminarClienteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Cliente")
        self.setGeometry(300, 300, 400, 200)
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
                background-color: #E74C3C;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)

        layout = QFormLayout()

        self.id_input = QLineEdit()
        eliminar_btn = QPushButton("Eliminar Cliente")
        eliminar_btn.clicked.connect(self.eliminar_cliente)

        layout.addRow("ID Cliente:", self.id_input)
        layout.addRow(eliminar_btn)

        self.setLayout(layout)

    def eliminar_cliente(self):
        cliente_id = self.id_input.text()
        if not cliente_id:
            QMessageBox.warning(self, "Error", "El ID del cliente es obligatorio.")
            return

        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar al cliente con ID {cliente_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            try:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
                conn.commit()
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente.")
                self.close()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar cliente: {e}")
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

class ActualizarVendedorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Actualizar Vendedor")
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

        self.id_input = QLineEdit()
        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Deja vacío para no cambiar la contraseña")

        buscar_btn = QPushButton("Buscar Vendedor")
        buscar_btn.clicked.connect(self.buscar_vendedor)

        guardar_btn = QPushButton("Actualizar Vendedor")
        guardar_btn.clicked.connect(self.actualizar_vendedor)

        layout.addRow("ID Vendedor:", self.id_input)
        layout.addRow("Username:", self.username_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Nueva Contraseña:", self.password_input)
        layout.addRow(buscar_btn)
        layout.addRow(guardar_btn)

        self.setLayout(layout)

    def buscar_vendedor(self):
        vendedor_id = self.id_input.text()
        if not vendedor_id:
            QMessageBox.warning(self, "Error", "El ID del vendedor es obligatorio.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT username, email FROM vendedores WHERE id = %s", (vendedor_id,))
            vendedor = cursor.fetchone()

            if vendedor:
                self.username_input.setText(vendedor[0])
                self.email_input.setText(vendedor[1])
            else:
                QMessageBox.warning(self, "Error", "Vendedor no encontrado.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al buscar vendedor: {e}")
        finally:
            cursor.close()
            conn.close()

    def actualizar_vendedor(self):
        vendedor_id = self.id_input.text()
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not vendedor_id or not username or not email:
            QMessageBox.warning(self, "Error", "Los campos ID, Username y Email son obligatorios.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()

            if password:
                cursor.execute("""
                    UPDATE vendedores
                    SET username = %s, email = %s, password_hash = SHA2(%s, 256)
                    WHERE id = %s
                """, (username, email, password, vendedor_id))
            else:
                cursor.execute("""
                    UPDATE vendedores
                    SET username = %s, email = %s
                    WHERE id = %s
                """, (username, email, vendedor_id))

            conn.commit()
            QMessageBox.information(self, "Éxito", "Vendedor actualizado correctamente.")
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar vendedor: {e}")
        finally:
            cursor.close()
            conn.close()


class EliminarVendedorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Vendedor")
        self.setGeometry(300, 300, 400, 200)
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
                background-color: #E74C3C;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)

        layout = QFormLayout()

        self.id_input = QLineEdit()
        eliminar_btn = QPushButton("Eliminar Vendedor")
        eliminar_btn.clicked.connect(self.eliminar_vendedor)

        layout.addRow("ID Vendedor:", self.id_input)
        layout.addRow(eliminar_btn)

        self.setLayout(layout)

    def eliminar_vendedor(self):
        vendedor_id = self.id_input.text()
        if not vendedor_id:
            QMessageBox.warning(self, "Error", "El ID del vendedor es obligatorio.")
            return

        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar al vendedor con ID {vendedor_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            try:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM vendedores WHERE id = %s", (vendedor_id,))
                conn.commit()
                QMessageBox.information(self, "Éxito", "Vendedor eliminado correctamente.")
                self.close()
            except mysql.connector.Error as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar vendedor: {e}")
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
                background-color: #F5F5DC;
            }
            QLabel {
                font-size: 24px;
                color: #2E4053;
                font-weight: bold;
                margin: 20px;
            }
        """)

        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: #E2725B; color: 5D4037; font-size: 14px;")

        # Menú de Clientes
        clientes_menu = menu_bar.addMenu("Clientes")
        agregar_cliente_action = QAction("Agregar Cliente", self)
        listar_clientes_action = QAction("Listar Clientes", self)
        actualizar_cliente_action = QAction("Actualizar Cliente", self)
        eliminar_cliente_action = QAction("Eliminar Cliente", self)

        clientes_menu.addAction(agregar_cliente_action)
        clientes_menu.addAction(listar_clientes_action)
        clientes_menu.addAction(actualizar_cliente_action)
        clientes_menu.addAction(eliminar_cliente_action)

        agregar_cliente_action.triggered.connect(self.agregar_cliente)
        listar_clientes_action.triggered.connect(self.listar_clientes)
        actualizar_cliente_action.triggered.connect(self.actualizar_cliente)
        eliminar_cliente_action.triggered.connect(self.eliminar_cliente)

        # Menú de Vendedores
        vendedores_menu = menu_bar.addMenu("Usuarios")
        agregar_vendedor_action = QAction("Agregar Vendedor", self)
        listar_vendedores_action = QAction("Listar Vendedores", self)
        actualizar_vendedor_action = QAction("Actualizar Vendedor", self)
        eliminar_vendedor_action = QAction("Eliminar Vendedor", self)

        vendedores_menu.addAction(agregar_vendedor_action)
        vendedores_menu.addAction(listar_vendedores_action)
        vendedores_menu.addAction(actualizar_vendedor_action)
        vendedores_menu.addAction(eliminar_vendedor_action)

        agregar_vendedor_action.triggered.connect(self.agregar_vendedor)
        listar_vendedores_action.triggered.connect(self.listar_vendedores)
        actualizar_vendedor_action.triggered.connect(self.actualizar_vendedor)
        eliminar_vendedor_action.triggered.connect(self.eliminar_vendedor)

        # Mensaje de bienvenida
        welcome_label = QLabel("🌟 Bienvenido al Sistema de Venta de Alfombras 🌟")
        welcome_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(welcome_label)
        
        # Menú de Productos
        productos_menu = menu_bar.addMenu("Productos")
        agregar_producto_action = QAction("Agregar Producto", self)
        listar_productos_action = QAction("Listar Productos", self)
        actualizar_producto_action = QAction("Actualizar Producto", self)
        eliminar_producto_action = QAction("Eliminar Producto", self)

        productos_menu.addAction(agregar_producto_action)
        productos_menu.addAction(listar_productos_action)
        productos_menu.addAction(actualizar_producto_action)
        productos_menu.addAction(eliminar_producto_action)

        agregar_producto_action.triggered.connect(self.agregar_producto)
        listar_productos_action.triggered.connect(self.listar_productos)
        actualizar_producto_action.triggered.connect(self.actualizar_producto)
        eliminar_producto_action.triggered.connect(self.eliminar_producto)

    # Métodos para Productos
    def agregar_producto(self):
        dialog = AgregarProductoDialog(self)
        dialog.exec_()

    def listar_productos(self):
        dialog = ListarProductosDialog(self)
        dialog.exec_()

    def actualizar_producto(self):
        dialog = ActualizarProductoDialog(self)
        dialog.exec_()

    def eliminar_producto(self):
        dialog = EliminarProductoDialog(self)
        dialog.exec_()

    # Métodos para Clientes
    def agregar_cliente(self):
        dialog = AgregarClienteDialog(self)
        dialog.exec_()

    def listar_clientes(self):
        dialog = ListarClientesDialog(self)
        dialog.exec_()

    def actualizar_cliente(self):
        dialog = ActualizarClienteDialog(self)
        dialog.exec_()
    
    def eliminar_cliente(self):
        dialog = EliminarClienteDialog(self)
        dialog.exec_()

    # Métodos para Vendedores
    def agregar_vendedor(self):
        dialog = AgregarVendedorDialog(self)
        dialog.exec_()

    def listar_vendedores(self):
        dialog = ListarVendedoresDialog(self)
        dialog.exec_()

    def actualizar_vendedor(self):
        dialog = ActualizarVendedorDialog(self)
        dialog.exec_()

    def eliminar_vendedor(self):
        dialog = EliminarVendedorDialog(self)
        dialog.exec_()


### --- EJECUCIÓN --- ###
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
