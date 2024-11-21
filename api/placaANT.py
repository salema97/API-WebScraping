import json
from flask import jsonify
import requests
from bs4 import BeautifulSoup
from api.JSONs import generar_json_placa


def consulta_placa(placa: str):
    data = []
    url = f"https://consultaweb.ant.gob.ec/PortalWEB/paginas/clientes/clp_grid_citaciones.jsp?ps_tipo_identificacion=PLA&ps_identificacion={placa}"

    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            elements = soup.find_all("td", class_=["detalle_formulario", "titulo2"])

            for td in elements:
                data.append(td.get_text())

            if data:
                return json.dumps(generar_json_placa(data))
            else:
                return json.dumps({})
        else:
            return json.dumps({"error": "Error al conectarse al sitio web."})
    except requests.exceptions.Timeout:
        return json.dumps({})
    except Exception as e:
        return json.dumps({})
