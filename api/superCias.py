from playwright.sync_api import sync_playwright
import time
import json


def consulta_compania(cedula: str):
    url = "https://appscvs1.supercias.gob.ec/consultaPersona/consulta_cia_param.zul"
    with sync_playwright() as p:
        browser = p.chromium.launch(
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

        page.click('label:text("Identificación")')
        cedula_input = page.wait_for_selector(".z-combobox-inp")
        cedula_input.fill(cedula)
        cedula_input.press("Backspace")
        tabla_selector = ".z-comboitem-text"

        time.sleep(0.8)
        if page.is_visible(tabla_selector) == True:
            page.wait_for_load_state()
            page.wait_for_selector(tabla_selector)
            page.click(tabla_selector)

            page.click(".z-button")
            page.wait_for_load_state()
            page.wait_for_selector(".z-listitem")

            page.query_selector(
                '//tr[@class="z-listitem"]/td[@class="z-listcell"]/div/span[@class="z-label"]'
            ).click()

            nueva_pagina = page.wait_for_event("popup")
            try:
                nueva_pagina.goto(nueva_pagina.url)
                nueva_pagina.wait_for_load_state()
                time.sleep(1.2)
                parte_constante = "frmInformacionCompanias:j_idt"
                elementos = nueva_pagina.query_selector_all(
                    f'//input[contains(@id, "{parte_constante}") and contains(@id, "j_idt")]'
                )
                valores_elementos = []
                for elemento in elementos:
                    valor_elemento = elemento.get_attribute("value")
                    valores_elementos.append(valor_elemento)
                result_dict = {
                    "ruc": valores_elementos[1],
                    "fecha_constitucion": valores_elementos[2],
                    "nacionalidad": valores_elementos[3],
                    "detalle_ubicacion": {
                        "provincia": valores_elementos[6].strip(),
                        "canton": valores_elementos[7].strip(),
                        "ciudad": valores_elementos[8].strip(),
                        "parroquia": valores_elementos[9].strip(),
                        "calle": valores_elementos[10].strip(),
                    },
                    "detalle_contacto": {
                        "celular": valores_elementos[23],
                        "telefono_1": valores_elementos[24].strip(),
                        "correo_1": valores_elementos[27].strip(),
                        "correo_2": valores_elementos[28].strip(),
                    },
                }

                browser.close()
            except Exception as e:
                return json.dumps({})
            return json.dumps(result_dict)
        else:
            return json.dumps({})
