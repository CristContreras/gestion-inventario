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

print(solicitar_texto("Ingrese texto", False))
