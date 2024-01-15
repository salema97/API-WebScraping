import os
from flask import Flask, render_template
from api.basico import consulta_aduna
from api.placaANT import consulta_placa
from api.predialLatacunga import consulta_predial
from api.superCias import consulta_compania
from api.datos import consulta

os.system("playwright install chromium")
os.system("playwright install-deps chromium")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/consulta/<cedula>")
def consultaDatos(cedula):
    return consulta(cedula)


@app.get("/consulta/placa/<placa>")
def consultaPlaca(placa):
    return consulta_placa(placa)


@app.get("/consulta/predial/<cedula>")
def consultaPredial(cedula):
    return consulta_predial(cedula)


@app.get("/consulta/superCias/<cedula>")
def consultaCompania(cedula):
    return consulta_compania(cedula)


@app.get("/consulta/basica/<cedula>")
def consultaBasica(cedula):
    return consulta_aduna(cedula)


if __name__ == "__main__":
    app.run()
