import json
import re


def generar_json_placa(data_list):
    if len(data_list) != 0:
        # Crear un diccionario con los datos de la lista
        datos_vehiculo = {
            "placa": data_list[0].strip(),
            "marca": data_list[1].strip(),
            "color": data_list[2].strip(),
            "anioMatricula": data_list[3].strip(),
            "detalles": {
                "modelo": data_list[5].strip(),
                "clase": data_list[6].strip(),
                "fechaMatricula": data_list[7].strip(),
                "anio": data_list[8].strip(),
                "servicio": data_list[9].strip(),
                "fechaCaducidad": data_list[10].strip(),
                "polarizado": data_list[11].strip(),
            },
        }

        # Convertir el diccionario a JSON
        json_data = json.dumps(datos_vehiculo)

        return json_data


def generar_json_predial(data_list, num_list):
    if len(data_list) != 0:
        # Crear un diccionario con los datos de la lista
        datos_predial = {
            "totalTerrenos": len(num_list),
            "predioPrincipal": {
                "claveCatastral": data_list[0].strip(),
                "zona": data_list[1].strip(),
                "area_m2": data_list[3].strip(),
                "areaConstruccion": data_list[4].strip(),
                "perimetro": data_list[7].strip(),
                "direccion": re.sub(r"\bNombre:\s*", "", data_list[8].strip()),
                "usoPredio": data_list[9].strip(),
            },
        }

        # Convertir el diccionario a JSON
        json_data = json.dumps(datos_predial)

        return json_data
