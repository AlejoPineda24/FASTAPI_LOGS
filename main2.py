from fastapi import FastAPI, Body, HTTPException
from datetime import datetime
import csv

app = FastAPI()

# Datos iniciales
productos = [
    {
        "codigo": 1,
        "nombre": "Mouse",
        "valor": 120000,
        "existencia": 10
    },
    {
        "codigo": 2,
        "nombre": "Teclado",
        "valor": 200000,
        "existencia": 15
    },
    {
        "codigo": 3,
        "nombre": "Monitor",
        "valor": 500000,
        "existencia": 12
    }
]

# Función de historial
def registrar_historial(accion: str, producto: dict, detalle: str):
    archivo_existe = False

    try:
        with open("historial.csv", "r"):
            archivo_existe = True
    except:
        archivo_existe = False

    with open("historial.csv", "a", newline='') as archivo:
        writer = csv.writer(archivo)

        # Si el archivo no existe, escribe encabezados
        if not archivo_existe:
            writer.writerow(["fecha", "accion", "detalle", "producto"])

        # Escribir fila
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            accion,
            detalle,
            str(producto)
        ])

# Endpoints básicos
@app.get('/')
def mensaje():
    return "Bienvenido a la tienda gamer"

@app.get('/{nombre}/{codigo}')
def mensaje2(nombre: str, codigo: int):
    return f"Bienvenido a la tienda gamer, {nombre}! Tu codigo es {codigo}."

@app.get('/uno')
def mensaje3(nombre: str, edad: int):
    return f"Bienvenido a la tienda gamer, {nombre}! Tu edad es {edad} años."

@app.get('/productos/')
def lista_productos():
    return productos

# Obtener producto por código
@app.get('/productos/codigo/{codigo}')
def obtener_producto(codigo: int):
    if codigo <= 0:
        raise HTTPException(status_code=400, detail="El código debe ser mayor que cero")
    
    for producto in productos:
        if producto["codigo"] == codigo:
            return producto
    
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Obtener producto por nombre
@app.get('/productos/nombre/{nombre}')
def obtener_producto_por_nombre(nombre: str):
    for producto in productos:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Crear producto
@app.post('/productos')
def crear_producto(
    nombre: str = Body(), 
    valor: int = Body(), 
    existencia: int = Body()
):
    if valor <= 0 or existencia < 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor que cero y la existencia no puede ser negativa")
    
    nuevo_codigo = max(producto['codigo'] for producto in productos) + 1
    
    nuevo_producto = {
        'codigo': nuevo_codigo,
        'nombre': nombre,
        'valor': valor,
        'existencia': existencia
    }

    productos.append(nuevo_producto)

    registrar_historial(
        "CREAR",
        nuevo_producto,
        "Producto creado correctamente"
    )

    return nuevo_producto

# Crear producto manual (mejorado)
@app.post('/productos2')
def crear_producto_manual(
    codigo: int = Body(), 
    nombre: str = Body(), 
    valor: float = Body(), 
    existencia: int = Body()
):
    for producto in productos:
        if producto["codigo"] == codigo:
            raise HTTPException(status_code=400, detail="El código ya existe")

    if valor <= 0 or existencia < 0:
        raise HTTPException(status_code=400, detail="Datos inválidos")

    nuevo_producto = {
        'codigo': codigo,
        'nombre': nombre,
        'valor': valor,
        'existencia': existencia
    }

    productos.append(nuevo_producto)

    registrar_historial(
        "CREAR",
        nuevo_producto,
        "Producto creado manualmente"
    )

    return nuevo_producto

# Actualizar producto
@app.put('/productos/{codigo}')
def actualizar_producto(
    codigo: int, 
    nombre: str = Body(), 
    valor: float = Body(),
    existencia: int = Body()
):
    if valor <= 0 or existencia < 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor que cero y la existencia no puede ser negativa") 

    for producto in productos:
        if producto['codigo'] == codigo:
            antes = producto.copy()

            producto['nombre'] = nombre
            producto['valor'] = valor
            producto['existencia'] = existencia

            registrar_historial(
                "ACTUALIZAR",
                {
                    "antes": antes,
                    "despues": producto
                },
                "Producto actualizado"
            )

            return {"antes": antes, "despues": producto}

    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Eliminar producto
@app.delete('/productos/{codigo}')
def eliminar_producto(codigo: int):
    for producto in productos:
        if producto['codigo'] == codigo:
            productos.remove(producto)

            registrar_historial(
                "ELIMINAR",
                producto,
                "Producto eliminado"
            )

            return {"mensaje": "Producto eliminado", "producto": producto}

    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Ver historial
@app.get('/historial')
def ver_historial():
    try:
        with open("historial.csv", "r") as archivo:
            return archivo.read()
    except:
        return {"mensaje": "No hay historial"}