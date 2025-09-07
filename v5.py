import sys
import json
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox,
                             QDialog, QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QMessageBox, QCheckBox, QFormLayout, QComboBox)

class Producto:
    """Clase para manejar productos."""
    def __init__(self, nombre, descripcion, categoria, presentacion, cantidad_por_presentacion,
                 unidad_medida, precio_compra, precio_venta, cantidad,
                 fecha_vencimiento, lote, temperatura, condiciones, medicamento_controlado, proveedor):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.presentacion = presentacion
        self.cantidad_por_presentacion = cantidad_por_presentacion
        self.unidad_medida = unidad_medida
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.cantidad = cantidad
        self.fecha_vencimiento = fecha_vencimiento
        self.lote = lote
        self.temperatura = temperatura
        self.condiciones = condiciones
        self.medicamento_controlado = medicamento_controlado
        self.proveedor = proveedor

    def a_diccionario(self):
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'presentacion': self.presentacion,
            'cantidad_por_presentacion': self.cantidad_por_presentacion,
            'unidad_medida': self.unidad_medida,
            'precio_compra': self.precio_compra,
            'precio_venta': self.precio_venta,
            'cantidad': self.cantidad,
            'fecha_vencimiento': self.fecha_vencimiento,
            'lote': self.lote,
            'temperatura': self.temperatura,
            'condiciones': self.condiciones,
            'medicamento_controlado': self.medicamento_controlado,
            'proveedor': self.proveedor
        }

    @staticmethod
    def de_diccionario(datos):
        return Producto(
            datos.get('nombre', ''),
            datos.get('descripcion', ''),
            datos.get('categoria', ''),
            datos.get('presentacion', ''),
            datos.get('cantidad_por_presentacion', 0),
            datos.get('unidad_medida', ''),
            datos.get('precio_compra', 0.0),
            datos.get('precio_venta', 0.0),
            datos.get('cantidad', 0),
            datos.get('fecha_vencimiento', ''),
            datos.get('lote', ''),
            datos.get('temperatura', ''),
            datos.get('condiciones', ''),
            datos.get('medicamento_controlado', False),
            datos.get('proveedor', '')
        )

class DialogoAgregarProducto(QDialog):
    """Diálogo para añadir un nuevo producto."""

    CATEGORIAS = {
        "Medicamentos (sólidos)": {
            "presentaciones": ["Tableta", "Cápsula", "Comprimido"],
            "unidades": ["mg", "g", "unidad", "blister", "caja"]
        },
        "Medicamentos (líquidos)": {
            "presentaciones": ["Jarabe", "Suspensión", "Gotas"],
            "unidades": ["ml", "L", "gotas", "frasco"]
        },
        "Inyectables": {
            "presentaciones": ["Ampolla", "Vial", "Carpule"],
            "unidades": ["ml", "unidad", "caja"]
        },
        "Tópicos": {
            "presentaciones": ["Crema", "Pomada", "Gel", "Spray", "Loción"],
            "unidades": ["g", "ml", "tubo", "frasco"]
        },
        "Supositorios/Óvulos": {
            "presentaciones": ["Supositorio", "Óvulo"],
            "unidades": ["unidad", "caja"]
        },
        "Parches/Inhaladores": {
            "presentaciones": ["Parche", "Inhalador"],
            "unidades": ["unidad", "dosis/inhalación", "caja"]
        },
        "Dispositivos médicos": {
            "presentaciones": ["Jeringa", "Guantes", "Mascarilla"],
            "unidades": ["unidad", "paquete", "caja"]
        },
        "Suplementos/Vitaminas": {
            "presentaciones": ["Tableta", "Cápsula", "Jarabe"],
            "unidades": ["mg", "g", "ml", "frasco", "blister", "caja"]
        },
        "Cuidado personal": {
            "presentaciones": ["Shampoo", "Jabón", "Crema"],
            "unidades": ["ml", "g", "frasco", "tubo", "caja"]
        },
        "Higiene/desinfección": {
            "presentaciones": ["Alcohol", "Gel antibacterial"],
            "unidades": ["ml", "L", "frasco", "galón"]
        },
        "Infantil": {
            "presentaciones": ["Pañales", "Fórmula láctea"],
            "unidades": ["unidad", "paquete", "lata", "caja"]
        },
        "Cosméticos": {
            "presentaciones": ["Maquillaje", "Bloqueador", "Perfume"],
            "unidades": ["ml", "g", "frasco", "tubo", "caja"]
        }
    }

    def __init__(self, productos_existentes):
        super().__init__()
        self.setWindowTitle("Añadir Producto")
        self.setFixedSize(400, 700)
        self.productos_existentes = productos_existentes

        # Campos de entrada
        self.nombre_producto = QLineEdit()
        self.descripcion_producto = QTextEdit()
        self.categoria = QComboBox()
        self.categoria.addItems(self.CATEGORIAS.keys())
        self.presentacion = QComboBox()
        self.unidad_medida = QComboBox()
        self.cantidad_por_presentacion = QLineEdit()
        self.precio_compra = QLineEdit()
        self.cantidad = QLineEdit()
        self.fecha_vencimiento = QLineEdit()
        self.lote = QLineEdit()
        self.temperatura = QLineEdit()
        self.condiciones = QLineEdit()
        self.medicamento_controlado = QCheckBox()
        self.proveedor = QLineEdit()

        # Relacionar combos
        self.categoria.currentTextChanged.connect(self.actualizar_presentacion_y_unidad)
        self.actualizar_presentacion_y_unidad(self.categoria.currentText())

        # Botón de guardar
        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar_producto)

        # Layout del formulario
        layout_formulario = QFormLayout()
        layout_formulario.addRow("Nombre del producto:", self.nombre_producto)
        layout_formulario.addRow("Descripción:", self.descripcion_producto)
        layout_formulario.addRow("Categoría:", self.categoria)
        layout_formulario.addRow("Presentación:", self.presentacion)
        layout_formulario.addRow("Cantidad por presentación:", self.cantidad_por_presentacion)
        layout_formulario.addRow("Unidad de medida:", self.unidad_medida)
        layout_formulario.addRow("Precio de compra:", self.precio_compra)
        layout_formulario.addRow("Cantidad en stock:", self.cantidad)
        layout_formulario.addRow("Fecha de vencimiento (YYYY-MM-DD):", self.fecha_vencimiento)
        layout_formulario.addRow("Lote:", self.lote)
        layout_formulario.addRow("Temperatura:", self.temperatura)
        layout_formulario.addRow("Condiciones:", self.condiciones)
        layout_formulario.addRow("Medicamento controlado:", self.medicamento_controlado)
        layout_formulario.addRow("Proveedor:", self.proveedor)
        layout_formulario.addRow(self.boton_guardar)

        self.setLayout(layout_formulario)
        self.producto = None

    def actualizar_presentacion_y_unidad(self, categoria):
        self.presentacion.clear()
        self.unidad_medida.clear()
        if categoria in self.CATEGORIAS:
            self.presentacion.addItems(self.CATEGORIAS[categoria]["presentaciones"])
            self.unidad_medida.addItems(self.CATEGORIAS[categoria]["unidades"])

    def guardar_producto(self):
        nombre = self.nombre_producto.text().strip()
        descripcion = self.descripcion_producto.toPlainText().strip()
        categoria = self.categoria.currentText()
        presentacion = self.presentacion.currentText()
        try:
            cantidad_por_presentacion = int(self.cantidad_por_presentacion.text().strip())
        except:
            cantidad_por_presentacion = 0
        unidad_medida = self.unidad_medida.currentText()
        try:
            precio_compra = float(self.precio_compra.text().strip())
        except:
            precio_compra = 0
        try:
            cantidad = int(self.cantidad.text().strip())
        except:
            cantidad = 0
        fecha_vencimiento = self.fecha_vencimiento.text().strip()
        lote = self.lote.text().strip()
        temperatura = self.temperatura.text().strip()
        condiciones = self.condiciones.text().strip()
        medicamento_controlado = self.medicamento_controlado.isChecked()
        proveedor = self.proveedor.text().strip()
        precio_venta = math.ceil(precio_compra * 1.3)

        if not nombre or not descripcion or not categoria or not presentacion or cantidad_por_presentacion <= 0 \
            or not unidad_medida or precio_compra <= 0 or precio_venta <= 0 or cantidad < 0 \
            or not fecha_vencimiento or not lote or not temperatura or not condiciones or not proveedor:
            QMessageBox.warning(self, "Entrada inválida", "Todos los campos son requeridos y deben ser válidos.")
            return

        if any(p.nombre.lower() == nombre.lower() for p in self.productos_existentes):
            QMessageBox.warning(self, "Entrada inválida", f"Ya existe un producto con el nombre '{nombre}'.")
            return

        self.producto = Producto(
            nombre, descripcion, categoria, presentacion, cantidad_por_presentacion,
            unidad_medida, precio_compra, precio_venta, cantidad,
            fecha_vencimiento, lote, temperatura, condiciones, medicamento_controlado, proveedor
        )
        QMessageBox.information(self, "Éxito", f"Producto '{nombre}' añadido correctamente.")
        self.accept()

class DialogoEditarProducto(QDialog):
    """Diálogo para editar un producto existente."""
    CATEGORIAS = DialogoAgregarProducto.CATEGORIAS

    def __init__(self, producto, productos_existentes, padre):
        super().__init__(padre)
        self.setWindowTitle("Editar Producto")
        self.setFixedSize(400, 700)
        self.producto = producto
        self.productos_existentes = productos_existentes

        self.nombre_producto = QLineEdit(self.producto.nombre)
        self.descripcion_producto = QTextEdit(self.producto.descripcion)
        self.categoria = QComboBox()
        self.categoria.addItems(self.CATEGORIAS.keys())
        self.presentacion = QComboBox()
        self.unidad_medida = QComboBox()
        self.cantidad_por_presentacion = QLineEdit(str(self.producto.cantidad_por_presentacion))
        self.precio_compra = QLineEdit(str(self.producto.precio_compra))
        self.cantidad = QLineEdit(str(self.producto.cantidad))
        self.fecha_vencimiento = QLineEdit(self.producto.fecha_vencimiento)
        self.lote = QLineEdit(self.producto.lote)
        self.temperatura = QLineEdit(self.producto.temperatura)
        self.condiciones = QLineEdit(self.producto.condiciones)
        self.medicamento_controlado = QCheckBox()
        self.medicamento_controlado.setChecked(self.producto.medicamento_controlado)
        self.proveedor = QLineEdit(self.producto.proveedor)
        self.precio_venta = QLabel(str(self.producto.precio_venta))

        # Relacionar combos
        self.categoria.currentTextChanged.connect(self.actualizar_presentacion_y_unidad)
        self.categoria.setCurrentText(self.producto.categoria)
        self.actualizar_presentacion_y_unidad(self.producto.categoria)
        if self.producto.presentacion in self.CATEGORIAS[self.producto.categoria]["presentaciones"]:
            self.presentacion.setCurrentText(self.producto.presentacion)
        else:
            self.presentacion.setCurrentIndex(0)
        if self.producto.unidad_medida in self.CATEGORIAS[self.producto.categoria]["unidades"]:
            self.unidad_medida.setCurrentText(self.producto.unidad_medida)
        else:
            self.unidad_medida.setCurrentIndex(0)

        self.boton_guardar = QPushButton("Guardar Cambios")
        self.boton_guardar.clicked.connect(self.guardar_producto)
        self.boton_eliminar = QPushButton("Eliminar Producto")
        self.boton_eliminar.clicked.connect(self.eliminar_producto)

        layout_formulario = QFormLayout()
        layout_formulario.addRow("Nombre del producto:", self.nombre_producto)
        layout_formulario.addRow("Descripción:", self.descripcion_producto)
        layout_formulario.addRow("Categoría:", self.categoria)
        layout_formulario.addRow("Presentación:", self.presentacion)
        layout_formulario.addRow("Cantidad por presentación:", self.cantidad_por_presentacion)
        layout_formulario.addRow("Unidad de medida:", self.unidad_medida)
        layout_formulario.addRow("Precio de compra:", self.precio_compra)
        layout_formulario.addRow("Precio de venta (calculado):", self.precio_venta)
        layout_formulario.addRow("Cantidad en stock:", self.cantidad)
        layout_formulario.addRow("Fecha de vencimiento (YYYY-MM-DD):", self.fecha_vencimiento)
        layout_formulario.addRow("Lote:", self.lote)
        layout_formulario.addRow("Temperatura:", self.temperatura)
        layout_formulario.addRow("Condiciones:", self.condiciones)
        layout_formulario.addRow("Medicamento controlado:", self.medicamento_controlado)
        layout_formulario.addRow("Proveedor:", self.proveedor)
        layout_formulario.addRow(self.boton_guardar)
        layout_formulario.addRow(self.boton_eliminar)

        self.setLayout(layout_formulario)

    def actualizar_presentacion_y_unidad(self, categoria):
        self.presentacion.clear()
        self.unidad_medida.clear()
        if categoria in self.CATEGORIAS:
            self.presentacion.addItems(self.CATEGORIAS[categoria]["presentaciones"])
            self.unidad_medida.addItems(self.CATEGORIAS[categoria]["unidades"])

    def guardar_producto(self):
        nombre = self.nombre_producto.text().strip()
        descripcion = self.descripcion_producto.toPlainText().strip()
        categoria = self.categoria.currentText()
        presentacion = self.presentacion.currentText()
        try:
            cantidad_por_presentacion = int(self.cantidad_por_presentacion.text().strip())
        except:
            cantidad_por_presentacion = 0
        unidad_medida = self.unidad_medida.currentText()
        try:
            precio_compra = float(self.precio_compra.text().strip())
        except:
            precio_compra = 0
        try:
            cantidad = int(self.cantidad.text().strip())
        except:
            cantidad = 0
        fecha_vencimiento = self.fecha_vencimiento.text().strip()
        lote = self.lote.text().strip()
        temperatura = self.temperatura.text().strip()
        condiciones = self.condiciones.text().strip()
        medicamento_controlado = self.medicamento_controlado.isChecked()
        proveedor = self.proveedor.text().strip()
        precio_venta = math.ceil(precio_compra * 1.3)

        if not nombre or not descripcion or not categoria or not presentacion or cantidad_por_presentacion <= 0 \
            or not unidad_medida or precio_compra <= 0 or precio_venta <= 0 or cantidad < 0 \
            or not fecha_vencimiento or not lote or not temperatura or not condiciones or not proveedor:
            QMessageBox.warning(self, "Entrada inválida", "Todos los campos son requeridos y deben ser válidos.")
            return

        if any(p.nombre.lower() == nombre.lower() for p in self.productos_existentes if p != self.producto):
            QMessageBox.warning(self, "Entrada inválida", f"Ya existe un producto con el nombre '{nombre}'.")
            return

        self.producto.nombre = nombre
        self.producto.descripcion = descripcion
        self.producto.categoria = categoria
        self.producto.presentacion = presentacion
        self.producto.cantidad_por_presentacion = cantidad_por_presentacion
        self.producto.unidad_medida = unidad_medida
        self.producto.precio_compra = precio_compra
        self.producto.precio_venta = precio_venta
        self.producto.cantidad = cantidad
        self.producto.fecha_vencimiento = fecha_vencimiento
        self.producto.lote = lote
        self.producto.temperatura = temperatura
        self.producto.condiciones = condiciones
        self.producto.medicamento_controlado = medicamento_controlado
        self.producto.proveedor = proveedor
        self.precio_venta.setText(str(precio_venta))
        QMessageBox.information(self, "Éxito", f"Producto '{nombre}' actualizado correctamente.")
        self.accept()

    def eliminar_producto(self):
        confirmacion = QMessageBox.question(self, "Eliminar Producto",
                                            f"¿Estás seguro de que deseas eliminar '{self.producto.nombre}'?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmacion == QMessageBox.Yes:
            self.producto = None
            self.accept()

class DialogoSeleccionarProductoStock(QDialog):
    """Diálogo para seleccionar un producto y añadir stock."""
    def __init__(self, productos, ventana_principal):
        super().__init__()
        self.setWindowTitle("Añadir Stock a Producto")
        self.setFixedSize(400, 300)
        self.productos = productos
        self.ventana_principal = ventana_principal

        # Barra de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Escribe el nombre del producto...")
        self.campo_busqueda.textChanged.connect(self.actualizar_resultados_busqueda)

        # Lista de resultados
        self.lista_resultados = QListWidget()
        self.lista_resultados.itemClicked.connect(self.abrir_dialogo_stock)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.campo_busqueda)
        layout.addWidget(self.lista_resultados)
        self.setLayout(layout)

        self.actualizar_resultados_busqueda()

    def actualizar_resultados_busqueda(self):
        texto_busqueda = self.campo_busqueda.text().strip().lower()
        self.lista_resultados.clear()
        if texto_busqueda:
            productos_coincidentes = [p for p in self.productos if texto_busqueda in p.nombre.lower()]
        else:
            productos_coincidentes = self.productos
        for producto in productos_coincidentes:
            self.lista_resultados.addItem(QListWidgetItem(producto.nombre))

    def abrir_dialogo_stock(self, item):
        nombre_producto = item.text()
        producto = next(p for p in self.productos if p.nombre == nombre_producto)

        dialogo = QDialog(self)
        dialogo.setWindowTitle(f"Añadir Stock a {producto.nombre}")
        dialogo.setFixedSize(300, 200)

        label_precio = QLabel("Precio de compra del nuevo lote:")
        input_precio = QLineEdit()
        label_cantidad = QLabel("Cantidad adquirida:")
        input_cantidad = QLineEdit()
        boton_aceptar = QPushButton("Añadir")
        boton_aceptar.clicked.connect(lambda: self.aceptar_stock(dialogo, producto, input_precio, input_cantidad))

        layout = QFormLayout()
        layout.addRow(label_precio, input_precio)
        layout.addRow(label_cantidad, input_cantidad)
        layout.addRow(boton_aceptar)
        dialogo.setLayout(layout)
        dialogo.exec_()

    def aceptar_stock(self, dialogo, producto, input_precio, input_cantidad):
        try:
            nuevo_precio = float(input_precio.text())
            nueva_cantidad = int(input_cantidad.text())
            if nuevo_precio <= 0 or nueva_cantidad <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Entrada inválida", "Ingrese valores válidos para precio y cantidad.")
            return

        # Promedio ponderado
        total_actual = producto.cantidad
        precio_actual = producto.precio_compra
        total_nuevo = total_actual + nueva_cantidad
        if total_nuevo == 0:
            precio_promedio = nuevo_precio
        else:
            precio_promedio = ((precio_actual * total_actual) + (nuevo_precio * nueva_cantidad)) / total_nuevo

        producto.cantidad += nueva_cantidad
        producto.precio_compra = precio_promedio
        producto.precio_venta = math.ceil(precio_promedio * 1.3)
        QMessageBox.information(self, "Stock añadido", f"Stock y precios actualizados correctamente.")
        self.ventana_principal.guardar_productos()
        dialogo.accept()

class DialogoMostrarTodosProductos(QDialog):
    """Diálogo para mostrar todos los productos registrados."""
    def __init__(self, productos, ventana_principal):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.setFixedSize(600, 500)
        self.productos = productos
        self.ventana_principal = ventana_principal

        # Lista de productos
        self.lista_productos = QListWidget()
        self.lista_productos.itemClicked.connect(self.mostrar_detalle_producto)
        self.actualizar_lista_productos()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.lista_productos)

        self.setLayout(layout)

    def actualizar_lista_productos(self):
        """Actualizar la lista de productos mostrados."""
        self.lista_productos.clear()
        productos_ordenados = sorted(self.productos, key=lambda p: p.nombre.lower())
        for producto in productos_ordenados:
            self.lista_productos.addItem(QListWidgetItem(
                f"{producto.nombre} | Cat: {producto.categoria} | Pres: {producto.presentacion} | "
                f"Stock: {producto.cantidad} | Vence: {producto.fecha_vencimiento} | Lote: {producto.lote}"
            ))

    def mostrar_detalle_producto(self, item):
        """Mostrar todos los detalles y permitir editar."""
        nombre_producto = item.text().split(" | ")[0]
        producto = next(p for p in self.productos if p.nombre == nombre_producto)
        dialogo_editar = DialogoEditarProducto(producto, self.productos, self)
        if dialogo_editar.exec_() == QDialog.Accepted:
            if dialogo_editar.producto is None:  # Si fue eliminado
                self.productos.remove(producto)
                self.ventana_principal.guardar_productos()
        self.actualizar_lista_productos()

class DialogoBuscarProducto(QDialog):
    """Diálogo para buscar productos."""
    def __init__(self, productos, dialogo_canasta):
        super().__init__()
        self.setWindowTitle("Buscar Producto")
        self.setFixedSize(400, 300)

        self.productos = productos
        self.dialogo_canasta = dialogo_canasta  # Guardamos una referencia a DialogoCanasta

        # Campo de búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Escribe el nombre del producto...")
        self.campo_busqueda.textChanged.connect(self.actualizar_resultados_busqueda)

        # Lista de resultados
        self.lista_resultados = QListWidget()
        self.lista_resultados.itemClicked.connect(self.mostrar_info_producto)

        # Layout del diálogo
        layout = QVBoxLayout()
        layout.addWidget(self.campo_busqueda)
        layout.addWidget(self.lista_resultados)

        self.setLayout(layout)
        self.actualizar_resultados_busqueda()  # Inicializar la lista de resultados

    def actualizar_resultados_busqueda(self):
        """Actualizar los resultados de búsqueda basados en la entrada."""
        texto_busqueda = self.campo_busqueda.text().strip().lower()
        self.lista_resultados.clear()

        if texto_busqueda:
            productos_coincidentes = [p for p in self.productos if p.nombre.lower().startswith(texto_busqueda)]
        else:
            productos_coincidentes = self.productos  # Mostrar todos si el campo está vacío

        for producto in productos_coincidentes:
            self.lista_resultados.addItem(QListWidgetItem(producto.nombre))

    def mostrar_info_producto(self, item):
        """Mostrar solo nombre, descripción, cantidad en stock y precio de venta."""
        nombre_producto = item.text()
        producto = next(p for p in self.productos if p.nombre == nombre_producto)

        # Calcular cantidad disponible real (restando lo que ya está en la canasta)
        en_canasta = next((item for item in self.dialogo_canasta.productos_en_canasta if item['producto'] == producto), None)
        cantidad_en_canasta = en_canasta['cantidad'] if en_canasta else 0
        cantidad_disponible = producto.cantidad - cantidad_en_canasta

        if cantidad_disponible == 0:
            QMessageBox.warning(self, "Sin stock", f"No hay unidades disponibles de '{producto.nombre}'.")
            return

        dialogo_cantidad = QDialog(self)
        dialogo_cantidad.setWindowTitle("Seleccionar Cantidad")
        dialogo_cantidad.setFixedSize(350, 200)

        layout_cantidad = QFormLayout()
        layout_cantidad.addRow("Producto:", QLabel(producto.nombre))
        layout_cantidad.addRow("Descripción:", QLabel(producto.descripcion))
        layout_cantidad.addRow("Stock disponible:", QLabel(str(cantidad_disponible)))
        layout_cantidad.addRow("Precio de venta:", QLabel(str(producto.precio_venta)))

        label_cantidad = QLabel("¿Cuántas unidades deseas llevar?")
        spin_cantidad = QSpinBox()
        spin_cantidad.setRange(0, cantidad_disponible)
        layout_cantidad.addRow(label_cantidad, spin_cantidad)

        boton_enviar = QPushButton("Enviar")
        boton_enviar.clicked.connect(lambda: self.confirmar_cantidad(dialogo_cantidad, producto, spin_cantidad.value()))
        layout_cantidad.addRow(boton_enviar)

        dialogo_cantidad.setLayout(layout_cantidad)
        dialogo_cantidad.exec_()

    def confirmar_cantidad(self, dialogo, producto, cantidad):
        """Confirma la cantidad y cierra el diálogo."""
        if cantidad <= 0:
            QMessageBox.warning(self, "Cantidad inválida", "Debes seleccionar al menos 1 unidad.")
            return
        # Agregar el producto con la cantidad seleccionada a la canasta
        if self.dialogo_canasta.agregar_producto(producto, cantidad):
            QMessageBox.information(self, "Cantidad Seleccionada", f"Has añadido {cantidad} unidad(es) de {producto.nombre}.")
            dialogo.accept()  # Cierra el diálogo de cantidad

class DialogoCanasta(QDialog):
    """Diálogo para manejar la canasta de productos."""
    def __init__(self,ventana_principal):
        super().__init__()
        self.ventana_principal = ventana_principal
        self.setWindowTitle("Canasta")
        self.setFixedSize(400, 400)
        self.productos_en_canasta = []  # Lista de productos en la canasta

        # Lista de productos en la canasta
        self.lista_canasta = QListWidget()
        self.lista_canasta.itemDoubleClicked.connect(self.editar_o_eliminar_producto_canasta)

        # Campo para introducir el monto de pago
        self.label_monto_pago = QLabel("Monto con el que se paga:")
        self.input_monto_pago = QLineEdit()
        self.input_monto_pago.setPlaceholderText("Ingrese el monto de pago")
        
        # Etiqueta para mostrar el total
        self.label_total = QLabel("Total a pagar: $0.00")
        
        # Botón para realizar el pago
        self.boton_pagar = QPushButton("Pagar")
        self.boton_pagar.clicked.connect(self.realizar_pago)

        # Layout del diálogo
        layout = QVBoxLayout()
        layout.addWidget(self.lista_canasta)
        layout.addWidget(self.label_total)  # Añadir la etiqueta de total
        layout.addWidget(self.label_monto_pago)
        layout.addWidget(self.input_monto_pago)
        layout.addWidget(self.boton_pagar)

        self.setLayout(layout)

    def editar_o_eliminar_producto_canasta(self, item):
        """Permite editar la cantidad o eliminar el producto de la canasta."""
        index = self.lista_canasta.row(item)
        producto_info = self.productos_en_canasta[index]
        producto = producto_info['producto']

        dialogo = QDialog(self)
        dialogo.setWindowTitle(f"Editar {producto.nombre}")
        dialogo.setFixedSize(250, 150)

        label = QLabel(f"Cantidad de '{producto.nombre}':")
        spin = QSpinBox()
        spin.setRange(0, producto.cantidad)
        spin.setValue(producto_info['cantidad'])

        boton_guardar = QPushButton("Guardar")
        boton_guardar.clicked.connect(lambda: dialogo.accept())
        boton_eliminar = QPushButton("Eliminar")
        boton_eliminar.clicked.connect(lambda: dialogo.done(2))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(spin)
        layout_h = QHBoxLayout()
        layout_h.addWidget(boton_guardar)
        layout_h.addWidget(boton_eliminar)
        layout.addLayout(layout_h)
        dialogo.setLayout(layout)

        resultado = dialogo.exec_()
        if resultado == QDialog.Accepted:
            nueva_cantidad = spin.value()
            if nueva_cantidad == 0:
                del self.productos_en_canasta[index]
            else:
                self.productos_en_canasta[index]['cantidad'] = nueva_cantidad
            self.actualizar_lista_canasta()
        elif resultado == 2:
            del self.productos_en_canasta[index]
            self.actualizar_lista_canasta()

    def agregar_producto(self, producto, cantidad):
        """Agregar un producto a la canasta."""
        en_canasta = next((item for item in self.productos_en_canasta if item['producto'] == producto), None)
        cantidad_en_canasta = en_canasta['cantidad'] if en_canasta else 0
        if cantidad <= 0:
            QMessageBox.warning(self, "Cantidad inválida", "Debes seleccionar al menos 1 unidad.")
            return False
        # Verificar si hay suficiente stock
        if cantidad + cantidad_en_canasta > producto.cantidad:
            QMessageBox.warning(self, "Stock insuficiente", 
                f"No puedes añadir {cantidad} unidades. Solo hay {producto.cantidad - cantidad_en_canasta} disponibles.")
            return False

        if en_canasta:
            en_canasta['cantidad'] += cantidad
        else:
            self.productos_en_canasta.append({'producto': producto, 'cantidad': cantidad})

        self.actualizar_lista_canasta()
        return True

    def actualizar_lista_canasta(self):
        """Actualizar la visualización de productos en la canasta y el total."""
        self.lista_canasta.clear()
        total = sum(item['cantidad'] * item['producto'].precio_venta for item in self.productos_en_canasta)
        self.label_total.setText(f"Total a pagar: ${total:.2f}")  # Actualizar total

        for item in self.productos_en_canasta:
            lista_item = f"{item['producto'].nombre} - {item['cantidad']} x {item['producto'].precio_venta} = {item['cantidad'] * item['producto'].precio_venta}"
            self.lista_canasta.addItem(lista_item)

    def realizar_pago(self):
        """Realizar el pago de los productos en la canasta."""
        total = sum(item['cantidad'] * item['producto'].precio_venta for item in self.productos_en_canasta)
        
        # Obtener el monto ingresado y calcular el vuelto
        try:
            monto_pago = float(self.input_monto_pago.text())
            if monto_pago < total:
                QMessageBox.warning(self, "Pago insuficiente", "El monto ingresado es insuficiente para cubrir el total.")
                return
            vuelto = monto_pago - total
            texto_pago = f"Total a pagar: ${total:.2f}\nMonto pagado: ${monto_pago:.2f}\nVuelto: ${vuelto:.2f}"
            
            for item in self.productos_en_canasta:
                item['producto'].cantidad -= item['cantidad']
                if item['producto'].cantidad < 0:
                    item['producto'].cantidad = 0

            # Confirmación de pago exitoso y limpieza de la canasta
            QMessageBox.information(self, "Pago realizado", texto_pago)
            self.productos_en_canasta.clear()
            self.actualizar_lista_canasta()
            self.input_monto_pago.clear()
            self.ventana_principal.guardar_productos()
        except ValueError:
            QMessageBox.warning(self, "Entrada inválida", "Por favor, ingrese un valor numérico válido en el campo de pago.")

class InventarioApp(QWidget):
    """Aplicación principal de gestión de inventario."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Inventario")
        self.setFixedSize(400, 300)

        self.productos = []

        # Cargar productos desde un archivo
        self.cargar_productos()

        self.dialogo_canasta = DialogoCanasta(self)

        # Botones
        self.boton_agregar = QPushButton("Agregar Producto")
        self.boton_agregar.clicked.connect(self.abrir_dialogo_agregar)

        self.boton_mostrar_inventario = QPushButton("Mostrar Inventario")
        self.boton_mostrar_inventario.clicked.connect(self.mostrar_inventario)

        self.boton_buscar = QPushButton("Buscar Producto")
        self.boton_buscar.clicked.connect(self.abrir_dialogo_buscar)

        self.boton_canasta = QPushButton("Canasta")
        self.boton_canasta.clicked.connect(self.abrir_dialogo_canasta)

        self.boton_anadir_stock = QPushButton("Añadir Stock")
        self.boton_anadir_stock.clicked.connect(self.abrir_dialogo_anadir_stock)
        

        # Layout de la ventana principal
        layout = QVBoxLayout()
        layout.addWidget(self.boton_agregar)
        layout.addWidget(self.boton_mostrar_inventario)
        layout.addWidget(self.boton_buscar)
        layout.addWidget(self.boton_canasta)
        layout.addWidget(self.boton_anadir_stock)

        self.setLayout(layout)

    def abrir_dialogo_agregar(self):
        """Abrir el diálogo para agregar un nuevo producto."""
        dialogo = DialogoAgregarProducto(self.productos)
        if dialogo.exec_() == QDialog.Accepted and dialogo.producto:
            self.productos.append(dialogo.producto)
            self.guardar_productos()
    
    def mostrar_inventario(self):
        dialogo = DialogoMostrarTodosProductos(self.productos, self)
        dialogo.exec_()
        
    def abrir_dialogo_buscar(self):
        """Abrir el diálogo para buscar productos."""
        dialogo_buscar = DialogoBuscarProducto(self.productos, self.dialogo_canasta)  # Pasar el diálogo de la canasta
        dialogo_buscar.exec_()

    def abrir_dialogo_canasta(self):
        self.dialogo_canasta.exec_()

    def cargar_productos(self):
        """Cargar productos desde un archivo JSON."""
        try:
            with open("productos.json", "r") as archivo:
                productos_data = json.load(archivo)
                self.productos = [Producto.de_diccionario(p) for p in productos_data]
        except FileNotFoundError:
            self.productos = []

    def guardar_productos(self):
        """Guardar productos en un archivo JSON."""
        with open("productos.json", "w") as archivo:
            json.dump([p.a_diccionario() for p in self.productos], archivo)

    def abrir_dialogo_anadir_stock(self):
        dialogo = DialogoSeleccionarProductoStock(self.productos, self)
        dialogo.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InventarioApp()
    ventana.show()
    sys.exit(app.exec_())