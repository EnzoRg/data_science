import csv
import json
import glob
import requests
from datetime import datetime

print(glob.glob('data_science/data_chacabuco_illia/*'))

# Se carga el archivo .json desde una url de Github
url = 'https://api.github.com/sebascoca/Proyecto_Mentoria-FaMAF_2024/tree/main/ChacabucoIllia_N'
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
    #dia_semana = dias_semana[c_data[2]]

    # Cantidad de vehículos
    cantidad_vehiculos = c_data[1]

    # Turno 
    turno = turno_raw.lower()

    # Horario
    if len(c_data) > 3:
        horario = horarios_raw[c_data[3]]
    else:
        horario = horario

    # Cantidad de vehículos
    cantidad_vehiculos = c_data[1]
    
    filas.append([fecha, turno, dia_semana, horario, cantidad_vehiculos])

# Se crea un nuevo archivo .csv
with open('datos.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    columnas = ['fecha', 'turno', 'dia_semana', 'horario', 'cantidad']
    
    # Se escriben el nombre las columnas y filas
    writer.writerow(columnas)
    writer.writerows(filas)
