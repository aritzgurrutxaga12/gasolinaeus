import json
import os
import time
import datetime
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = context
        return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)


URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/"
FICHERO_JSON = "precios_gasolineras.json"


def descargar_datos():
    session = requests.Session()
    session.mount("https://", SSLAdapter())

    ultimo_error = None

    for intento in range(1, 4):
        try:
            print(f"Intento {intento}/3 descargando precios...")
            r = session.get(URL, timeout=60)
            r.raise_for_status()
            datos = r.json()["ListaEESSPrecio"]
            print(f"Descarga correcta. Registros: {len(datos)}")
            return datos

        except Exception as e:
            ultimo_error = e
            print(f"Error en intento {intento}/3: {e}")
            if intento < 3:
                time.sleep(20)

    raise ultimo_error


def main():
    try:
        datos = descargar_datos()

        payload = {
            "fecha_descarga": datetime.datetime.now().isoformat(),
            "datos": datos
        }

        with open(FICHERO_JSON, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)

        print("precios_gasolineras.json actualizado correctamente.")

    except Exception as e:
        print(f"No se ha podido actualizar desde la API: {e}")

        if os.path.exists(FICHERO_JSON):
            print("Se mantiene el JSON existente. No se rompe el workflow.")
            return

        raise


if __name__ == "__main__":
    main()
