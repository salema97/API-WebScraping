import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def consulta_sri(cedula: str):
    url = "https://calculadoras.trabajo.gob.ec/impedimento"
    datos = {}

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

        page.locator("#txtNumeroDocumento").fill(cedula)
        page.get_by_text("Buscar").click()

        page.wait_for_selector("#txtNombreCompelto")

        soup = str(BeautifulSoup(page.inner_html("body"), "html.parser"))

        print(soup)

        datos["nombres"] = str(
            page.eval_on_selector("#txtNombreCompelto", "label => label.innerText;")
        )

        datos["cedula"] = cedula

        browser.close()

        print(json.dumps(datos))

    return json.dumps(datos)


consulta_sri("0550243737")
