import os
from flask import Flask, render_template
from api.placa import consulta_placa
from api.predial import consulta_predial

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/consulta/placa/<placa>")
def consultaPlaca(placa):
    return consulta_placa(placa)


@app.get("/consulta/predial/<cedula>")
def consultaPredial(cedula):
    return consulta_predial(cedula)


if __name__ == "__main__":
    os.system("playwright install chromium")
    os.system("playwright install-deps chromium")
    app.run()
