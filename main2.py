from fastapi import FastAPI, Body, HTTPException
from datetime import datetime
import json

app = FastAPI()

productos = [
    {
        "codigo" : 1,
        "nombre" : "Mouse",
        "valor" : 120000,
        "existencia" : 10
    },
    {
        "codigo" : 2,
        "nombre" : "Teclado",
        "valor" : 200000,
        "existencia" : 15
    },
    {
        "codigo" : 3,
        "nombre" : "Monitor",
        "valor" : 500000,
        "existencia" : 12
    }
]

def registrar_historial(accion: str, producto: dict, detalle: str):
    log = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accion": accion,
        "detalle": detalle,
        "producto": producto
    }

    with open("historial.txt", "a") as archivo:
        archivo.write(json.dumps(log) + "\n")

@app.get('/')
def mensaje():
    return "Bienvenido a la tieda gaymer "

@app.get('/{nombre}/{codigo}')
def mensaje2(nombre: str, codigo: int):
    return f"Bienvenido a la tienda gaymer, {nombre}! Tu codigo es {codigo}."

@app.get('/uno')
def mensaje3(nombre: str, edad: int):
    return f"Bienvenido a la tienda  gaymer, {nombre}! Tu edad es {edad} años."

@app.get('/productos/')
def listadeproductos():
    return productos


#Validacion 1 codigo debe ser mayor que cero
@app.get('/productos/codigo/{codigo}')
def obtener_producto(codigo: int):
    if codigo <= 0:
            raise HTTPException(status_code=400, detail="El código debe ser mayor que cero")
    for producto in productos:
        if producto["codigo"] == codigo:
            return producto
        
#Validacion 2 cuando el producto no se encuentra
@app.get('/productos/nombre/{nombre}')
def obtener_producto_por_nombre(nombre: str):
    for producto in productos:
        if producto["nombre"] == nombre:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")   

@app.post('/productos')
def crearProductos( 
    nombre: str = Body(), 
    valor: int = Body(), 
    existencia: int = Body()):
    #Validacion 3 consecutivo automatico del codigo
    if valor <= 0 or existencia < 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor que cero y la existencia no puede ser negativa")
        
    #Validacion 4 el valor debe ser mayor que cero y la existencia no puede ser negativa
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

@app.post('/productos2')
def crearProductos2(
    codigo:int=Body(), 
    nombre:str=Body(), 
    valor:float=Body(), 
    existencia:int=Body()):
    productos.append({
        'codigo': codigo,
        'nombre': nombre,
        'valor': valor,
        'existencia': existencia
    }
    )
    return productos

#Validacion 5 actualizar un producto por su codigo, si el producto no se encuentra, retornar un error
@app.put('/productos/{codigo}')
def actualizar_producto(codigo: int, 
    nombre: str = Body(), 
    valor: float = Body(),
    existencia: int = Body()):
    #Validacion 6 el valor debe ser mayor que cero y la existencia no puede ser negativa
    if valor <= 0 or existencia <= 0:
        raise HTTPException(status_code=400, detail="El valor debe ser mayor que cero y la existencia no puede ser negativa") 
    #Validacion 7 retornar el producto antes y despues de la actualizacion  
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
            return {"antes" : antes, "despues" : producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

#Validacion 8 eliminar un producto por su codigo, si el producto no se encuentra, retornar un error
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