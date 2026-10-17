
import os
import getpass
import requests

# Evaluacion N. 2 - GraphHopper
# Programa de rutas e indicaciones en espanol

GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"

SALIDAS = ("s", "salir")
TRANSPORTES = {
    "car": "Automovil",
    "bike": "Bicicleta",
    "foot": "A pie"
}


def pedir_ubicacion(mensaje):
    while True:
        ubicacion = input(mensaje).strip()

        if ubicacion.lower() in SALIDAS:
            return None

        if ubicacion:
            return ubicacion

        print("La ubicacion no puede estar vacia.")


def geocoding(ubicacion, clave):
    parametros = {
        "q": ubicacion,
        "limit": 1,
        "key": clave
    }

    try:
        respuesta = requests.get(
            GEOCODE_URL,
            params=parametros,
            timeout=30
        )
        datos = respuesta.json()

    except (requests.exceptions.RequestException, ValueError):
        print("Error de conexion con GraphHopper.")
        return None

    if respuesta.status_code != 200:
        print("Error de geocodificacion:",
              datos.get("message", "Error desconocido"))
        return None

    resultados = datos.get("hits", [])

    if not resultados:
        print("No se encontraron resultados para la ubicacion.")
        return None

    lugar = resultados[0]
    punto = lugar.get("point", {})

    if "lat" not in punto or "lng" not in punto:
        print("No se encontraron coordenadas validas.")
        return None

    nombre = lugar.get("name", ubicacion)

    return punto["lat"], punto["lng"], nombre


def calcular_ruta(origen, destino, transporte, clave):
    parametros = [
        ("point", f"{origen[0]},{origen[1]}"),
        ("point", f"{destino[0]},{destino[1]}"),
        ("profile", transporte),
        ("locale", "es"),
        ("instructions", "true"),
        ("key", clave)
    ]

    try:
        respuesta = requests.get(
            ROUTE_URL,
            params=parametros,
            timeout=30
        )
        datos = respuesta.json()

    except (requests.exceptions.RequestException, ValueError):
        print("Error al consultar la ruta en GraphHopper.")
        return None

    if respuesta.status_code != 200:
        print("Error al calcular la ruta:",
              datos.get("message", "Error desconocido"))
        return None

    rutas = datos.get("paths", [])

    if not rutas:
        print("No se encontro una ruta disponible.")
        return None

    return rutas[0]


def mostrar_ruta(ruta, origen, destino, transporte):
    kilometros = ruta.get("distance", 0) / 1000
    millas = kilometros / 1.609344

    segundos = int(ruta.get("time", 0) / 1000)
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos_restantes = segundos % 60

    print("\n========================================")
    print("RESULTADO DEL VIAJE")
    print("========================================")
    print("Origen:", origen[2])
    print("Destino:", destino[2])
    print("Transporte:", TRANSPORTES[transporte])

    print(f"Distancia: {kilometros:.2f} km")
    print(f"Distancia en millas: {millas:.2f}")
    print(
        f"Duracion estimada: "
        f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"
    )

    print("\nINSTRUCCIONES PASO A PASO")
    print("----------------------------------------")

    instrucciones = ruta.get("instructions", [])

    if not instrucciones:
        print("No hay instrucciones disponibles.")

    for numero, instruccion in enumerate(instrucciones, 1):
        texto = instruccion.get(
            "text", "Instruccion no disponible"
        )

        distancia = instruccion.get("distance", 0) / 1000

        print(f"{numero}. {texto}")
        print(f"   Distancia del tramo: {distancia:.2f} km")

    print("========================================")


def main():
    print("========================================")
    print("SISTEMA DE RUTAS GRAPHHOPPER")
    print("EVALUACION N. 2")
    print("========================================")

    clave = os.environ.get(
        "GRAPHHOPPER_API_KEY", ""
    ).strip()

    if not clave:
        clave = getpass.getpass(
            "Ingrese su API Key de GraphHopper: "
        ).strip()

    if not clave:
        print("No se ingreso una clave de API.")
        return

    while True:
        print("\n========================================")
        print("MEDIOS DE TRANSPORTE")
        print("========================================")
        print("car  - Automovil")
        print("bike - Bicicleta")
        print("foot - A pie")
        print("s o salir - Terminar el programa")

        transporte = input(
            "\nSeleccione un medio de transporte: "
        ).strip().lower()

        if transporte in SALIDAS:
            print("Programa finalizado correctamente.")
            break

        if transporte not in TRANSPORTES:
            print("Opcion no valida. Se usara automovil.")
            transporte = "car"

        ubicacion_origen = pedir_ubicacion(
            "\nIngrese la ciudad de origen (s/salir): "
        )

        if ubicacion_origen is None:
            print("Programa finalizado correctamente.")
            break

        origen = geocoding(ubicacion_origen, clave)

        if origen is None:
            print("Intente nuevamente.")
            continue

        ubicacion_destino = pedir_ubicacion(
            "Ingrese la ciudad de destino (s/salir): "
        )

        if ubicacion_destino is None:
            print("Programa finalizado correctamente.")
            break

        destino = geocoding(ubicacion_destino, clave)

        if destino is None:
            print("Intente nuevamente.")
            continue

        print("\nCalculando ruta, espere por favor...")

        ruta = calcular_ruta(
            origen, destino, transporte, clave
        )

        if ruta is None:
            print("No fue posible calcular el viaje.")
            continue

        mostrar_ruta(
            ruta, origen, destino, transporte
        )

        print("\nPuede consultar otra ruta.")
        print("Escriba s o salir para terminar.")


if __name__ == "__main__":
    main()
