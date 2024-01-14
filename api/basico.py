from datetime import datetime
import json
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def consulta_sri(cedula: str):
    url = "https://calculadoras.trabajo.gob.ec/impedimento"
    datos = {}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--start-maximized",
                "--blink-settings=imagesEnabled=false",
                "--disable-extensions",
            ],
        )
        page = browser.new_page()
        page.goto(url)

        page.locator("#txtNumeroDocumento").fill(cedula)
        page.get_by_text("Buscar").click()

        page.wait_for_selector("#txtNombreCompelto")

        nombres_value = page.evaluate(
            '(document.getElementById("txtNombreCompelto")).value'
        )
        datos["nombre"] = nombres_value.strip() if nombres_value else None
        datos["cedula"] = cedula

        browser.close()

    return json.dumps(datos)
