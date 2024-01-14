import requests
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json


def consulta_cedula_vehiculo(cedula: str):
    url = f"https://consultaweb.ant.gob.ec/PortalWEB/paginas/clientes/clp_grid_citaciones.jsp?ps_tipo_identificacion=CED&ps_identificacion={cedula}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        td_elements = soup.find_all(
            "td", class_=["titulo1", "MarcoTitulo", "detalle_formulario"]
        )
        if len(td_elements) != 0:
            data = {
                "nombre": td_elements[0].get_text(strip=True)
                if len(td_elements) > 0
                else None,
                "puntos": td_elements[2].get_text(strip=True)
                if len(td_elements) > 2
                else None,
                "tipo_licencia": td_elements[4].get_text(strip=True)
                if len(td_elements) > 4
                else None,
                "detalle_auto": None,  # Inicializamos a None por si no se encuentra una placa
            }
            # data_json = json.dumps(data, ensure_ascii=False, indent=4)

            with sync_playwright() as p:
                browser = p.chromium.launch(
                    args=[
                        "--disable-gpu",
                        "--start-maximized",
                        "--blink-settings=imagesEnabled=false",
                        "--disable-extensions",
                    ],
                )
                page = browser.new_page()
                page.goto(url)

                try:
                    radio_button_pendiente = page.wait_for_selector(
                        '//input[@type="radio" and @value="P"]'
                    )
                    radio_button_pendiente.click()

                    time.sleep(2)
                    elements = page.query_selector_all(
                        '//td[@aria-describedby="list10_secuencia_4"]'
                    )

                    if len(elements) > 0:
                        pass
                    else:
                        radio_button = page.wait_for_selector(
                            '//input[@type="radio" and @value="G"]'
                        )
                        radio_button.click()
                        time.sleep(2)
                        elements = page.query_selector_all(
                            '//td[@aria-describedby="list10_secuencia_4"]'
                        )
                        pass

                    placa = None
                    for element in elements:
                        text = element.text_content().strip()
                        if text and text != "-":
                            placa = text
                            break

                    if placa:
                        url_placa = f"https://consultaweb.ant.gob.ec/PortalWEB/paginas/clientes/clp_grid_citaciones.jsp?ps_tipo_identificacion=PLA&ps_identificacion={placa}"
                        response = requests.get(url_placa)

                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, "html.parser")
                            td_elements = soup.find_all(
                                "td", class_=["detalle_formulario", "titulo2"]
                            )
                            data_list = [td.get_text(strip=True) for td in td_elements]

                            data_auto = {
                                "placa": data_list[0],
                                "marca": data_list[1],
                                "color": data_list[2],
                                "año_matricula": data_list[3],
                                "modelo": data_list[5],
                                "clase": data_list[6],
                                "fecha_matricula": data_list[7],
                                "año": data_list[8],
                                "servicio": data_list[9],
                                "fecha_caducidad": data_list[10],
                                "polarizado": data_list[11],
                            }

                            data["detalle_auto"] = data_auto
                        else:
                            print("No se encontraron datos para la placa.")
                except Exception as e:
                    print(f"Datos no encontrados: {str(e)}")

            return json.dumps(data, ensure_ascii=False, indent=4)
        else:
            return json.dumps({})
    else:
        return json.dumps({"error": "Error al conectarse al sitio web"})
