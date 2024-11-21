import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from api.JSONs import generar_json_predial
from lxml import etree


def consulta_predial(cedula: str):
    url = "http://186.46.158.7/portal_EC/latacunga.php"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
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

        try:
            page.wait_for_selector("#map", timeout=15000)
            page.eval_on_selector("#map", "element => element.remove()")

            page.get_by_text("Cedula/Ruc").click()
            page.get_by_placeholder("Ingrese información").fill(cedula)
            page.get_by_text("Buscar").click()

            page.wait_for_timeout(200)
            if not page.is_visible(".swal2-header"):
                page.wait_for_selector("#prediosCiu", timeout=15000)
                page.wait_for_selector("#rpt_prediocatas1", timeout=15000)
                soup = str(BeautifulSoup(page.inner_html("body"), "html.parser"))
                browser.close()

                datos_Ciu = etree.HTML(soup).xpath(
                    "//div[@id='prediosCiu']//tr/td[1]/text()"
                )
                datos_Ciu.remove(datos_Ciu[0])
                datos_Predio = etree.HTML(soup).xpath(
                    "//div[@id='rpt_prediocatas1']/text()"
                )

                return generar_json_predial(datos_Predio, datos_Ciu)
            else:
                return json.dumps({})
        except Exception as e:
            browser.close()
            return json.dumps({})
