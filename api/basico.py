from datetime import datetime
import json
from playwright.sync_api import sync_playwright


def consulta_sri(cedula: str):
    url = "https://srienlinea.sri.gob.ec/sri-en-linea/SriPagosWeb/ConsultaDeudasFirmesImpugnadas/Consultas/consultaDeudasFirmesImpugnadas"
    result_dict = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-gpu",
                "--start-maximized",
                "--blink-settings=imagesEnabled=false",
                "--disable-extensions",
            ],
        )
        page = browser.new_page()
        page.goto(url)

        page.locator("#busquedaRucId").fill(cedula)
        page.wait_for_load_state()

        browser.close()

    return json.dumps(result_dict)


consulta_sri("0550243737")
