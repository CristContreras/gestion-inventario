import os
import sqlite3
import time as t


def limpiar_consola():
    """
    Limpia la consola
    """
    os.system("cls")


def mostrar_menu():
    """
    Muestra el titulo y el menu por consola
    """
    limpiar_consola()
    print("1. Registrar producto")
    print("2. Visualizar datos de los productos")
    print("3. Actualizar datos de productos")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Reporte productos")
    print("7. Salir")

def solicitar_texto(mensaje: str, puede_ser_nulo: bool):
    repetir = True
    while repetir:
        texto = input(mensaje)
        if puede_ser_nulo and texto == "":
            return None
        if not puede_ser_nulo and texto == "":
            return "-"
        else:
            repetir = False
    return texto

def solicitar_numero(mensaje: str, tipo_dato: str, puede_ser_nulo: bool):
    repetir = True
    numero=None
    while repetir:
        texto = input(mensaje)
        if puede_ser_nulo and texto=="":
            return None
        if not puede_ser_nulo and texto=="":
            return 0
        try:
            if "int" in tipo_dato:
                numero = int(texto)
            elif "float" in tipo_dato:
                numero=float(texto)
            repetir=False
        except ValueError:
            print("Imposible convertir a número")               
    return numero

def solicitar_datos() -> tuple[str, str, int, float, str]:
    """
    Solicita datos al usuario y los devuelve

    Returns:
        tuple[str, str, int, float, str]: Devuelve una tupla con los datos ingresados
    """
    repetir = True
    while repetir:
        nombre_producto = solicitar_texto("Ingrese nombre producto: ", False)
        if es_producto_existente(nombre_producto):
            print("El producto ya existe en la base de datos")
            t.sleep(3)
            limpiar_consola()
        else:
            descripcion = solicitar_texto("Ingrese descripcion: ", True)
            cantidad = solicitar_numero("Ingrese cantidad del producto: ", "int", False)
            precio = solicitar_numero("Ingrese precio del prodcuto: ", "float", False)
            categoria = solicitar_texto("Ingrese categoria del producto: ", True)
            repetir=False
            return nombre_producto, descripcion, cantidad, precio, categoria

def procesar_registro_producto():
    """
    LLeva adelante el registro solicitando datos de entrada y registrando el producto
    """
    print("Registrar nuevo producto\n")
    nombre_producto, descripcion, cantidad, precio, categoria = solicitar_datos()
    respuesta=registrar_producto(nombre_producto, descripcion, cantidad, precio, categoria)
    print(respuesta)
    t.sleep(3)

def procesar_visualización_productos():
    productos: list = obtener_productos()
    mostrar_productos(productos)
    t.sleep(5)



def registrar_producto(
    nombre_producto: str, descripcion: str, cantidad: int, precio: float, categoria: str
) -> str:
    """
    Registra un producto

    Args:
        nombre_producto (str): Nombre del producto tipo string
        descripcion (str): Descripcion del producto tipo string
        cantidad (int): Cantidad disponible del producto
        precio (float): Precio del producto
        categoria (str): Categoria del producto

    Returns:
        str: Si fue registrado o no con exito
    """
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    try:
        conexion.execute("BEGIN TRANSACTION")
        cursor.execute(
            "INSERT INTO productos (nombre_producto, descripcion, cantidad, precio, categoria) VALUES (?,?,?,?,?)",
            (nombre_producto, descripcion, cantidad, precio, categoria),
        )
        conexion.commit()
        return "Producto registrado con exito!"
    except sqlite3.Error as e:
        conexion.rollback()
        return f"Operación abortada por un error. Haciendo rollback - {e}"
    finally:
        conexion.close()

def obtener_productos() -> list[tuple]:
    try:
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos: list[tuple] = cursor.fetchall()
        return productos
    finally:
        conexion.close()

def mostrar_productos(productos: list) -> None:
    """
    Muestra por consola los productos de la lista

    Args:
        productos (list[tuple]): Lista de productos obtenidos de la base
    """
    if len(productos) == 0:
        print("No hay productos")
    else:
        for producto in productos:
            print(
                f"ID: {producto[0]}\nNombre producto {producto[1]}\nDescripción: {producto[2]}\nCantidad: {producto[3]}\nPrecio: ${producto[4]}\nCategoria: {producto[5]}\n\n"
            )

def crear_db() -> None:
    """
    Crea la base de datos y la tabla productos
    """
    conexion = sqlite3.connect("inventario.db")
    _crear_tabla_db(conexion.cursor())
    _commit_and_close(conexion)


def _crear_tabla_db(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""CREATE TABLE IF NOT EXISTS productos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre_producto TEXT NOT NULL,
                   descripcion TEXT,
                   cantidad INTEGER NOT NULL,
                   precio REAL NOT NULL,
                   categoria TEXTO)
""")


def _commit_and_close(conexion: sqlite3.Connection) -> None:
    """
    Hace el commit y cierra la conexion de la base de datos

    Args:
        conexion (sqlite3.Connection): Objeto conexion abierta de la base de datos
    """
    conexion.commit()
    conexion.close()

def mostrar_opciones_actualizacion():
    print("Elija una opción a actualizar")
    print("1. Nombre producto")
    print("2. Descripción")
    print("3. Cantidad")
    print("4. Precio")
    print("5. Categoria")



def procesar_actualización_producto():
    print("Productos disponibles")
    productos = obtener_productos()
    mostrar_productos(productos)

    id = solicitar_numero("Ingrese el ID del producto que quiere modificar: ", "int", False)
    
    producto_seleccionado=None
    
    limpiar_consola()

    for producto in productos:
        if producto[0]==id:
            producto_seleccionado=producto
    
    if producto_seleccionado is None:
        print("Error el producto no fue encontrado")
    else:
        repetir = True
        while repetir:
            mostrar_opciones_actualizacion()
            opcion=solicitar_numero("Ingrese la opcion a actualizar: ", "int", False)
            match(opcion):
                case 1:
                    nombre = solicitar_texto("Ingrese nuevo nombre: ", False)
                    actualizar_por_id(id,"nombre_producto",nombre)
                    print("Actualización correcta!")
                    repetir=False
                case 2:
                    descripcion = solicitar_texto("Ingrese nueva descripción: ", True)
                    actualizar_por_id(id,"descripcion",descripcion)
                    print("Actualización correcta!")
                    repetir=False
                case 3:
                    cantidad = solicitar_numero("Ingrese nueva cantidad: ", False)
                    actualizar_por_id(id,"cantidad",cantidad)
                    print("Actualización correcta!")
                    repetir=False
                case 4:
                    precio = solicitar_numero("Ingrese nuevo precio: ", False)
                    actualizar_por_id(id,"precio",precio)
                    print("Actualización correcta!")
                    repetir=False
                case 5:
                    categoria = solicitar_texto("Ingrese nueva categoria: ", True)
                    actualizar_por_id(id,"categoria",categoria)
                    print("Actualización correcta!")
                    repetir=False
                case _:
                    print("Opcion incorrecta")

def actualizar_por_id(id, campo, dato):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute(f"UPDATE productos SET {campo} = ? WHERE id = ?", (dato, id))
    _commit_and_close(conexion)

def procesar_eliminacion_producto():
    print("Productos disponibles")
    productos = obtener_productos()
    mostrar_productos(productos)

    id = solicitar_numero("Ingrese el ID del producto que quiere eliminar: ", "int", False)
    
    producto_seleccionado=None
    
    limpiar_consola()

    for producto in productos:
        if producto[0]==id:
            producto_seleccionado=producto
    
    if producto_seleccionado is None:
        print("Error el producto no fue encontrado")
    else:
        eliminar_por_id(id)
        print("Producto eliminado correctamente!")
        t.sleep(3)

def eliminar_por_id(id):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    _commit_and_close(conexion)

def procesar_busqueda_producto():
    print("1. ID")
    print("2. Nombre")
    print("3. Categoria")
    opcion = solicitar_numero("Ingrese la opcion por busqueda: ", "int", False)
    if opcion == 1:
        id = solicitar_numero("Ingrese el ID del producto: ", "int", False)
        producto = buscar_por_id(id)
        if producto is None:
            print("No se encontro el producto")
            t.sleep(3)
        else:
            print(
                f"ID: {producto[0]}\nNombre producto {producto[1]}\nDescripción: {producto[2]}\nCantidad: {producto[3]}\nPrecio: ${producto[4]}\nCategoria: {producto[5]}\n\n"
            )
        t.sleep(3)

    if opcion==2:
        nombre = solicitar_texto("Ingrese el nombre del producto: ",False)
        productos = buscar_por_nombre(nombre)
        mostrar_productos(productos)
        t.sleep(3)

    
    if opcion==3:
        categoria = solicitar_texto("Ingrese la categoria: ",False)
        productos = buscar_por_categoria(categoria)
        mostrar_productos(productos)
        t.sleep(3)


def buscar_por_id(id):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return producto

def buscar_por_categoria(categoria):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE categoria LIKE ?", (f"%{categoria}%",))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def es_producto_existente(nombre)->bool:
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre_producto= ?", (nombre,))
    producto = cursor.fetchone()
    conexion.close()
    return producto is not None

def buscar_por_nombre(nombre):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre_producto LIKE ?", (f"%{nombre}%",))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def procesar_reporte_stock_bajo():
    limite = solicitar_numero("Ingrese el límite de cantidad: ", "int", False)
    productos = buscar_por_stock_limite(limite)
    mostrar_productos(productos)
    t.sleep(3)

def buscar_por_stock_limite(limite):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    conexion.close()
    return productos

