from playwright.sync_api import sync_playwright

# from api.diccionario import generar_json_predial
import time
from bs4 import BeautifulSoup
import json


def consulta_predial(cedula: str):
    url = "https://gadmaapps.ambato.gob.ec:9001/apex/f?p=102:81:9116084841838:::81::"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            args=[
                "--disable-gpu",
                "--start-maximized",
                "--blink-settings=imagesEnabled=false",
                "--disable-extensions",
            ],
        )

        page = browser.new_page()
        page.goto(url)

        page.click('label:text("Cédula")')

        page.fill('input[name="P81_CAMPO"]', cedula)
        page.click("#B71736013380222400")

        page.wait_for_selector(".u-tL")
        datos_Predio = page.inner_html("id=193259360981438559_orig")
        browser.close()

        soup = BeautifulSoup(datos_Predio, "html.parser")

        datos = []

        filas = soup.find_all("tr")
        for fila in filas:
            celdas = fila.find_all("td")
            if celdas:
                data = {
                    "Dirección": celdas[0].text.strip(),
                    "Área Terreno": celdas[2].text.strip(),
                    "Avalúo Total": celdas[6].text.strip(),
                    "Tipo Predio": celdas[7].text.strip(),
                    "Parroquia": celdas[8].text.strip(),
                }
                datos.append(data)
        json_data = json.dumps(datos, ensure_ascii=False, indent=4)

        return json_data


cedula_consulta = "1802769305"
resultado = consulta_predial(cedula_consulta)
print(resultado)
