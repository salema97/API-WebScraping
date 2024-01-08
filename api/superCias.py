import json
from playwright.sync_api import sync_playwright


def consulta_compania(cedula: str):
    url = "https://appscvs1.supercias.gob.ec/consultaPersona/consulta_cia_param.zul"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            args=[
                "--disable-gpu",
                "--start-maximized",
                "--blink-settings=imagesEnabled=false",
                "--disable-extensions",
            ],
        )
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.click('label:text("Identificación")')
        cedula_input = page.wait_for_selector(".z-combobox-inp")
        cedula_input.fill(cedula)
        cedula_input.press("Backspace")
        tabla_selector = ".z-comboitem-text"
        page.wait_for_selector(tabla_selector)
        page.click(tabla_selector)
        page.click(".z-button")
        page.wait_for_selector(".z-listitem")
        datos_tabla = page.query_selector_all(
            '//tr[@class="z-listitem"]/td[@class="z-listcell"]'
        )
        result_dict = {}
        for dato in datos_tabla:
            dato.evaluate("(element) => element.textContent")
        enlace = page.query_selector(
            '//tr[@class="z-listitem"]/td[@class="z-listcell"]/div/span[@class="z-label"]'
        )
        enlace.click()
        nueva_pagina = page.wait_for_event("popup")
        # time.sleep(2)
        try:
            nueva_pagina.goto(nueva_pagina.url)

            # Obtener datos generales
            result_dict["expediente"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt114"]', "value"
            ).strip()
            result_dict["ruc"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt119"]', "value"
            ).strip()
            result_dict["fecha_de_constitución"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt124"]', "value"
            ).strip()
            result_dict["nacionalidad"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt129"]', "value"
            ).strip()
            result_dict["plazo_social"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt134"]', "value"
            ).strip()
            result_dict["oficina_control"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt139"]', "value"
            ).strip()

            # Obtener datos de ubicación
            result_dict["provincia"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt160"]', "value"
            ).strip()
            result_dict["canton"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt165"]', "value"
            ).strip()
            result_dict["ciudad"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt170"]', "value"
            ).strip()
            result_dict["parroquia"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt175"]', "value"
            ).strip()
            result_dict["calle"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt185"]', "value"
            ).strip()
            result_dict["referencia_ubicacion"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt235"]', "value"
            ).strip()
            result_dict["interseccion"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt190"]', "value"
            ).strip()
            result_dict["barrio"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt210"]', "value"
            )
            # contactos
            result_dict["telefono1"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt256"]', "value"
            ).strip()
            result_dict["correo1"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt271"]', "value"
            ).strip()
            result_dict["telefono2"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt261"]', "value"
            ).strip()
            result_dict["correo2"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt276"]', "value"
            ).strip()
            result_dict["celular"] = nueva_pagina.get_attribute(
                'input[id="frmInformacionCompanias:j_idt103:j_idt251"]', "value"
            ).strip()

            browser.close()

        except Exception as e:
            print(f"Datos no encontrados: {str(e)}")
        return json.dumps(result_dict)
