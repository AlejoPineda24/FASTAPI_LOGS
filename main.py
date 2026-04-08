from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def mensaje():
    return 'oli'

@app.get('/{nombre}/{codigo}')
def mensaje_n_c(nombre:str,codigo:int):
    return f'Bienvenido {nombre} su codigo es {codigo}'

@app.get('/uno')
def mensaje_edad(edad:int):
    return f'tu edad es {edad}'

@app.get('/dos')
def mensaje_E (estatura:float,peso:float):
    while estatura <= 1.70:
        if peso >70.0:
            return f'Tras de que mide {estatura} esta gordo  {peso} ?'
    while estatura > 1.70: 
        if peso <=65.0:
            return f'Buena estatura bro {estatura} pero no estaria mal comer'
        else:
            return f'Buena estatura bro {estatura} pero cuida el peso pa'