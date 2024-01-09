from concurrent.futures import ThreadPoolExecutor
import json
#from api.basicov2 import consulta_siirs
from api.predialLatacunga import consulta_predial
from api.superCias import consulta_compania
from api.vehiculo import consulta_cedula_vehiculo


def consulta(cedula: str):
    with ThreadPoolExecutor() as executor:
        # Se ejecutan las funciones de consulta de forma paralela
        # basico_future = executor.submit(consulta_siirs, cedula)
        vehiculo_future = executor.submit(consulta_cedula_vehiculo, cedula)
        predial_future = executor.submit(consulta_predial, cedula)
        cias_future = executor.submit(consulta_compania, cedula)

    # Obtener los resultados de las consultas
    # basico = json.loads(basico_future.result())
    vehiculo = json.loads(vehiculo_future.result())
    predial = json.loads(predial_future.result())
    cias = json.loads(cias_future.result())

    # Combinar los resultados
    # cias.update(basico)
    cias.update(vehiculo)
    cias.update(predial)

    return json.dumps(cias)
