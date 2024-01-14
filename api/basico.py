from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from playwright_recaptcha import recaptchav2
from bs4 import BeautifulSoup
from lxml import etree
import time


def consulta_siirs(cedula: str):
    url = "https://siirs.registrosocial.gob.ec/pages/publico/busquedaPublica.jsf"

    with sync_playwright() as playwright:
        try:
            browser = playwright.firefox.launch(
                headless=False,
                args=[
                    "--disable-gpu",
                    "--start-maximized",
                    # "--blink-settings=imagesEnabled=false",
                    "--disable-extensions",
                ],
            )
            page = browser.new_page()
            stealth_sync(page)
            page.goto(url)

            with recaptchav2.SyncSolver(
                page, capsolver_api_key="CAP-71A22A0C4D2FAE840D43FE4814DA6670"
            ) as solver:
                solver.solve_recaptcha(wait=True, image_challenge=True)
                page.locator("#frmBusquedaPublica\:txtCedula").fill(cedula)
                page.locator("#frmBusquedaPublica\:btnBuscar").click()
                time.sleep(2)
                page.wait_for_load_state()
                # page.wait_for_load_state("load", timeout=10000)
                soup = str(BeautifulSoup(page.inner_html("body"), "html.parser"))

                datos_casa = etree.HTML(soup).xpath(
                    "//span[@class='textoResultado']/text()"
                )
                table_data = etree.HTML(soup).xpath("//table[@role='grid']//tr")

                for row in table_data:
                    cell_values = row.xpath(".//td/text()")
                    if len(cell_values) >= 4 and cell_values[3].strip() == cedula:
                        # Se encontró la fila con la cédula completa
                        return cell_values

                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if browser:
                browser.close()


cedula = "0550243737"
salida = consulta_siirs(cedula)
print(salida)
