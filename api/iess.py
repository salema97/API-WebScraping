from datetime import datetime
import json
from playwright.sync_api import sync_playwright


def consulta_iess(cedula: str):
    url = "https://app.iess.gob.ec/gestion-calificacion-derecho-web/public/formulariosContacto.jsf"
    now = datetime.now()
    formatted_date = now.strftime("%d/%m/%Y")
    result_dict = {}

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

        page.locator("#formConsulta\:cedula_text").fill(cedula)
        page.evaluate(
            f"document.getElementById('formConsulta:fec_calendar_input').value = '{formatted_date}';"
        )
        page.wait_for_load_state()
        page.dblclick("#formConsulta\:contingencia_select_label")
        page.wait_for_load_state()
        page.dblclick("#formConsulta\:contingencia_select_2")
        page.wait_for_load_state()
        page.dblclick("#formConsulta\:j_idt40")

        page.wait_for_selector("#formConsulta\:j_idt52")

        result_dict["covertura"] = str(
            page.eval_on_selector("#formConsulta\:j_idt52", "label => label.innerText;")
        )

        result_dict["cedula"] = str(
            page.get_attribute('input[id="formConsulta:j_idt74"]', "value")
        )
        result_dict["nombres"] = str(
            page.get_attribute('input[id="formConsulta:j_idt78"]', "value")
        )
        result_dict["tipo_afiliacion"] = str(
            page.get_attribute('input[id="formConsulta:j_idt82"]', "value")
        )

        browser.close()

    return json.dumps(result_dict)
