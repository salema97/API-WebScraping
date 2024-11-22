import json
import time
from playwright.sync_api import sync_playwright


def consulta_aduna(cedula: str):
    url = "https://www.aduana.gob.ec/consultacupos/"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-gpu",
                "--start-maximized",
                "--blink-settings=imagesEnabled=false",
                "--disable-extensions",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ],
        )
        page = browser.new_page()
        page.goto(url)

        page.click("#exampleRadios1")
        page.locator("#txtCedula").fill(cedula)
        page.get_by_text("Consultar").click()

        try:
            page.wait_for_selector("#dato_cedula", timeout=10000)
            ced = page.text_content("id=dato_cedula")
            nombre = page.text_content("id=dato_nombre")

            if not ced or not nombre:
                datos_basico = {}
            else:
                datos_basico = {
                    "cedula": ced,
                    "nombre": nombre,
                }
        except:
            datos_basico = {}

        browser.close()
        return json.dumps(datos_basico)
