import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_async
from playwright_recaptcha import recaptchav2
from lxml import etree

from api.JSONs import generar_json_datos


def consulta_siirs(cedula: str):
    url = "https://siirs.registrosocial.gob.ec/pages/publico/busquedaPublica.jsf"

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(
            args=[
                "--disable-gpu",
                "--start-maximized",
                # "--blink-settings=imagesEnabled=false",
                "--disable-extensions",
            ],
        )
        page = browser.new_page()
        stealth_async(page)
        page.goto(url)

        with recaptchav2.SyncSolver(page) as solver:
            try:
                solver.solve_recaptcha(wait=True)
                page.locator("#frmBusquedaPublica\:txtCedula").fill(cedula)
                page.locator("#frmBusquedaPublica\:btnBuscar").click()

                page.wait_for_load_state()
                soup = str(BeautifulSoup(page.inner_html("body"), "html.parser"))
                browser.close()

                datos_casa = etree.HTML(soup).xpath(
                    "//span[@class='textoResultado']/text()"
                )
                datos_ciu = etree.HTML(soup).xpath(
                    "//tr[@class='ui-widget-content ui-datatable-even'][last()]/td/text()"
                )

                return generar_json_datos(datos_casa, datos_ciu)
            except:
                return json.dumps({})
