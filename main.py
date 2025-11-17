import core.utilidades.funciones as f


def main():
    f.crear_db()
    repetir = True
    while repetir:
        f.limpiar_consola()
        f.mostrar_menu()
        opcion = f.solicitar_numero("Seleccione una opción: ", "int", False)
        f.limpiar_consola()
        match opcion:
            case 1:
                f.procesar_registro_producto()
            case 2:
                f.procesar_visualización_productos()
            case 3:
                f.procesar_actualización_producto()
            case 4:
                f.procesar_eliminacion_producto()
            case 5:
                f.procesar_busqueda_producto()
            case 6:
                f.procesar_reporte_stock_bajo()
            case 7:
                print("Muchas gracias por utilizar el programa.\nSaliendo...")
                f.t.sleep(3)
                repetir = False
                f.limpiar_consola()
            case _:
                print("Opción incorrecta")
                f.t.sleep(2)


if __name__ == "__main__":
    main()
