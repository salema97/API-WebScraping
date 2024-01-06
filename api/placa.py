import requests
from bs4 import BeautifulSoup
from api.diccionario import generar_json_placa


def consulta_placa(placa: str):
    data = []
    url = f"https://consultaweb.ant.gob.ec/PortalWEB/paginas/clientes/clp_grid_citaciones.jsp?ps_tipo_identificacion=PLA&ps_identificacion={placa}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        elements = soup.find_all("td", class_=["detalle_formulario", "titulo2"])

        for td in elements:
            data.append(td.get_text())

        return generar_json_placa(data)
    else:
        return {"error": "Error al conectarse al sitio web."}
