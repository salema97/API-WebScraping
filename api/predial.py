from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from api.diccionario import generar_json_predial
from lxml import etree
import time


def consulta_predial(cedula: str):
    url = "http://186.46.158.7/portal_EC/latacunga.php"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        page.get_by_text("Cedula/Ruc").click()
        page.get_by_placeholder("Ingrese información").fill(cedula)
        page.get_by_text("Buscar").click()

        time.sleep(1)
        soup = str(BeautifulSoup(page.inner_html("body"), "html.parser"))
        browser.close()

        datos_Ciu = etree.HTML(soup).xpath("//div[@id='prediosCiu']//tr/td[1]/text()")
        datos_Ciu.remove(datos_Ciu[0])
        datos_Predio = etree.HTML(soup).xpath("//div[@id='rpt_prediocatas1']/text()")

        return generar_json_predial(datos_Predio, datos_Ciu)
