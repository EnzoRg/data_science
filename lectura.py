import json
import csv
import requests
from datetime import datetime

# Se carga el archivo .json desde una url de Github
url = 'https://raw.githubusercontent.com/sebascoca/Proyecto_Mentoria-FaMAF_2024/main/ChacabucoIllia_N/2019.11.2.json'
file = json.loads(requests.get(url).text)

# Se crean las rutas donde estan los datos de interes
dm0 = file['results'][0]['result']['data']['dsr']['DS'][0]['PH'][0]['DM0']
value_dicts = file['results'][0]['result']['data']['dsr']['DS'][0]['ValueDicts']

# Se crean las variables con los datos 
fechas_raw = value_dicts['D0']
turno_raw = value_dicts['D1'][0]
vehiculos_raw = value_dicts['D2']
dias_raw = value_dicts['D3']
fecha_data_raw = value_dicts['D4']
horarios_raw = value_dicts['D5']

# Se crea un diccionario para mapear los días de la semana
# Quizas cuando se implemente ML es mejor dejarlo como un float 
dias_semana = {
    0: "lunes",
    1: "martes",
    2: "miercoles",
    3: "jueves",
    4: "viernes",
    5: "sabado",
    6: "domingo"
}

# Se crea una lista vacia para insertar las nuevas filas
filas = []

# Se itera sobre el vector DM0
for x in dm0:
    # Se toma el valor de C
    c_data = x['C']

    # Fecha 
    fecha = fechas_raw[c_data[0]]

    # Día de la semana
    dia_numero = datetime.strptime(fecha, '%d/%m/%Y').weekday()
    dia_semana = dias_semana[dia_numero]

    # Cantidad de vehículos
    cantidad_vehiculos = c_data[1]

    # Turno 
    turno = turno_raw.lower()

    filas.append([fecha, cantidad_vehiculos, turno, dia_semana])

# Se crea un nuevo archivo .csv
with open('datos.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    columnas = ['fecha', 'cantidad', 'turno', 'dia_semana']
    
    # Se escriben el nombre las columnas y filas
    writer.writerow(columnas)
    writer.writerows(filas)

    #Prueba