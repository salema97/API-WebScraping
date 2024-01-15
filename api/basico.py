import json
import time
from playwright.sync_api import sync_playwright


def consulta_aduna(cedula: str):
    url = "https://www.aduana.gob.ec/consultacupos/"
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

        page.click("#exampleRadios1")
        page.locator("#txtCedula").fill(cedula)
        page.get_by_text("Consultar").click()
        page.wait_for_selector("#dato_cedula")

        ced = page.text_content("id=dato_cedula")
        nombre = page.text_content("id=dato_nombre")
        datos_basico = {
            "cedula": ced,
            "nombre": nombre,
        }

        browser.close()
        return json.dumps(datos_basico)
