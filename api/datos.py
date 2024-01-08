import json

# from api.iess import consulta_iess
from api.predialLatacunga import consulta_predial
from api.superCias import consulta_compania
from api.vehiculo import consulta_cedula_vehiculo


def consulta(cedula: str):
    # consulta_iess(cedula)
    vehiculo = json.loads(consulta_cedula_vehiculo(cedula))
    predial = json.loads(consulta_predial(cedula))
    cias = json.loads(consulta_compania(cedula))

    cias.update(vehiculo)
    cias.update(predial)

    return json.dumps(cias)
