import sys
import mysql.connector
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QMessageBox, QDialog, 
    QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog 
)

# Conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ORACLE",  # Cambia según tu configuración
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
    def __init__(self, parent=None, mostrar_confirmar=False):
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
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #16A085;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #34495E;
                border-radius: 10px;
            }
        """)

        self.layout = QVBoxLayout()

        # Campo de búsqueda
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("Ingrese clave del producto...")
        self.layout.addWidget(self.busqueda_input)

        # Botón de búsqueda
        buscar_btn = QPushButton("Buscar por clave")
        buscar_btn.clicked.connect(self.buscar_por_clave)
        self.layout.addWidget(buscar_btn)

        # Tabla de productos
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Código", "Nombre", "Descripción", "Precio", "Stock"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.layout.addWidget(self.table)

        # Botón para confirmar selección (opcional)
        if mostrar_confirmar:
            self.confirmar_btn = QPushButton("Confirmar Selección")
            self.confirmar_btn.clicked.connect(self.confirmar_seleccion)
            self.layout.addWidget(self.confirmar_btn)

        self.setLayout(self.layout)
        self.cargar_productos()

        # Variable para almacenar el producto seleccionado
        self.producto_seleccionado = None

    def cargar_productos(self):
        """Carga todos los productos de la base de datos en la tabla."""
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

    def buscar_por_clave(self):
        """Filtra los productos en la tabla según la clave del producto."""
        clave_producto = self.busqueda_input.text()
        if not clave_producto:
            QMessageBox.warning(self, "Error", "Debe ingresar una clave de producto.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, codigo_producto, nombre, descripcion, precio, stock FROM productos WHERE codigo_producto = %s",
                (clave_producto,)
            )
            producto = cursor.fetchone()

            if producto:
                self.table.setRowCount(1)
                for col_idx, col_data in enumerate(producto):
                    self.table.setItem(0, col_idx, QTableWidgetItem(str(col_data)))
            else:
                QMessageBox.information(self, "Sin resultados", "No se encontró un producto con esa clave.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al buscar producto: {e}")
        finally:
            cursor.close()
            conn.close()

    def confirmar_seleccion(self):
        """Confirma la selección del producto y cierra el diálogo."""
        selected_row = self.table.currentRow()
        if selected_row != -1:
            self.producto_seleccionado = {
                "id": int(self.table.item(selected_row, 0).text()),
                "codigo": self.table.item(selected_row, 1).text(),
                "nombre": self.table.item(selected_row, 2).text(),
                "precio": float(self.table.item(selected_row, 4).text()),
                "stock": int(self.table.item(selected_row, 5).text())
            }
            self.accept()  # Cerrar el diálogo con confirmación
        else:
            QMessageBox.warning(self, "Error", "Debe seleccionar un producto.")


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

### --- DIÁLOGOS PARA Facturacion --- ###     
class CrearFacturaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Factura")
        self.setGeometry(300, 300, 600, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #F5F5F5;
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
            QTableWidget {
                background-color: #ECF0F1;
                border: 2px solid #34495E;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #1ABC9C;
                color: white;
                font-size: 14px;
            }
        """)

        # Layout principal
        self.layout = QVBoxLayout()

        # Campos para cliente
        self.cliente_input = QLineEdit()
        self.cliente_input.setPlaceholderText("Buscar Cliente por ID")
        buscar_cliente_btn = QPushButton("Buscar Cliente")
        buscar_cliente_btn.clicked.connect(self.buscar_cliente)
        self.cliente_label = QLabel("Cliente no seleccionado")

        # Tabla para productos
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Nombre", "Cantidad", "Subtotal"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Botones para agregar productos y generar factura
        agregar_producto_btn = QPushButton("Agregar Producto")
        agregar_producto_btn.clicked.connect(self.agregar_producto)
        generar_factura_btn = QPushButton("Generar Factura")
        generar_factura_btn.clicked.connect(self.generar_factura)

        # Total
        self.total_label = QLabel("Total: $0.00")

        # Agregar widgets al layout
        self.layout.addWidget(QLabel("Buscar Cliente"))
        self.layout.addWidget(self.cliente_input)
        self.layout.addWidget(buscar_cliente_btn)
        self.layout.addWidget(self.cliente_label)
        self.layout.addWidget(QLabel("Productos"))
        self.layout.addWidget(self.table)
        self.layout.addWidget(agregar_producto_btn)
        self.layout.addWidget(self.total_label)
        self.layout.addWidget(generar_factura_btn)

        self.setLayout(self.layout)

        # Variables para cliente y total
        self.cliente_id = None
        self.total = 0.00

    def buscar_cliente(self):
        cliente_id = self.cliente_input.text()
        if not cliente_id:
            QMessageBox.warning(self, "Error", "Debe ingresar el ID del cliente.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM clientes WHERE id = %s", (cliente_id,))
            cliente = cursor.fetchone()
            if cliente:
                self.cliente_label.setText(f"Cliente: {cliente[0]}")
                self.cliente_id = cliente_id
            else:
                QMessageBox.information(self, "Cliente no encontrado", "El cliente no existe. Por favor, regístrelo.")
                dialog = AgregarClienteDialog(self)
                dialog.exec_()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al buscar cliente: {e}")
        finally:
            cursor.close()
            conn.close()

    def agregar_producto(self):
     dialog = ListarProductosDialog(self, mostrar_confirmar=True)
     if dialog.exec_() == QDialog.Accepted and dialog.producto_seleccionado:
        producto = dialog.producto_seleccionado
        cantidad, ok = QInputDialog.getInt(
            self, "Cantidad", 
            f"Ingrese cantidad para {producto['nombre']} (Stock: {producto['stock']}):",
            1, 1, producto['stock']
        )
        if ok:
            subtotal = cantidad * producto['precio']
            self.total += subtotal
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(producto['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(producto['codigo']))
            self.table.setItem(row, 2, QTableWidgetItem(producto['nombre']))
            self.table.setItem(row, 3, QTableWidgetItem(str(cantidad)))
            self.table.setItem(row, 4, QTableWidgetItem(f"${subtotal:.2f}"))
            self.total_label.setText(f"Total: ${self.total:.2f}")



    def generar_factura(self):
        if not self.cliente_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar un cliente.")
            return

        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Error", "Debe agregar al menos un producto.")
            return

        try:
            conn = conectar_db()
            cursor = conn.cursor()

            # Insertar factura
            cursor.execute("INSERT INTO facturas (cliente_id, vendedor_id, total) VALUES (%s, %s, %s)",
                           (self.cliente_id, 1, self.total))
            factura_id = cursor.lastrowid

            # Insertar detalles de factura
            for row in range(self.table.rowCount()):
                producto_id = int(self.table.item(row, 0).text())
                cantidad = int(self.table.item(row, 3).text())
                subtotal = float(self.table.item(row, 4).text().strip("$"))
                cursor.execute("""
                    INSERT INTO detalle_facturas (factura_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (factura_id, producto_id, cantidad, subtotal / cantidad, subtotal))

            conn.commit()
            QMessageBox.information(self, "Éxito", "Factura generada correctamente.")
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al generar factura: {e}")
        finally:
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
        agregar_vendedor_action = QAction("Agregar Usuario", self)
        listar_vendedores_action = QAction("Listar Usuarios", self)
        actualizar_vendedor_action = QAction("Actualizar Usuario", self)
        eliminar_vendedor_action = QAction("Eliminar Usuario", self)

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

        # Menú de Facturación
        facturacion_menu = menu_bar.addMenu("Facturación")
        crear_factura_action = QAction("Crear Factura", self)
        facturacion_menu.addAction(crear_factura_action)
        crear_factura_action.triggered.connect(self.crear_factura)

    # Metodo Facturacion
    def crear_factura(self):
        dialog = CrearFacturaDialog(self)
        dialog.exec_()
        
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
