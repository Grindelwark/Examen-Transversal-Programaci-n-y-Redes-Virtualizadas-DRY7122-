import requests
import urllib.parse
from math import radians, sin, cos, sqrt, atan2

API_KEY = "1d1a6faf-4f99-4217-8937-b087ffcf66df"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def geocodificar(ciudad):
    url = GEOCODE_URL + urllib.parse.urlencode({'q': ciudad, 'limit': '1', 'key': API_KEY})
    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()
        if not datos["hits"]:
            print(f"⚠️ No se encontró la ciudad: {ciudad}")
            return None
        hit = datos["hits"][0]
        lat, lon = hit["point"]["lat"], hit["point"]["lng"]
        nombre = f"{hit['name']}, {hit.get('state', '')}, {hit.get('country', '')}".strip(", ")
        return lat, lon, nombre
    except Exception as e:
        print(f"❌ Error al geocodificar '{ciudad}': {e}")
        return None

def distancia_aerea(lat1, lon1, lat2, lon2):
    radio = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return radio * c

def ruta_terrestre(origen, destino, tipo_transporte):
    puntos = f"&point={origen[0]},{origen[1]}&point={destino[0]},{destino[1]}"
    parametros = urllib.parse.urlencode({'vehicle': tipo_transporte, 'key': API_KEY})
    url_ruta = ROUTE_URL + parametros + puntos
    try:
        response = requests.get(url_ruta)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error al obtener la ruta terrestre: {e}")
        return None

def mostrar_terrestre(data, origen, destino, medio):
    path = data["paths"][0]
    km = path["distance"] / 1000
    millas = km / 1.61
    tiempo = int(path["time"] / 1000)
    hrs, rem = divmod(tiempo, 3600)
    mins, segs = divmod(rem, 60)

    print(f"\n📍 Desde: {origen}")
    print(f"🏁 Hasta: {destino}")
    print(f"🚙 Transporte: {medio}")
    print(f"📏 Distancia: {km:.2f} km / {millas:.2f} mi")
    print(f"⏱️ Duración estimada: {hrs:02d}:{mins:02d}:{segs:02d}")
    print(f"📝 Narrativa: El viaje por tierra desde {origen} a {destino} en {medio} cubre {km:.1f} km en {hrs}h {mins}m.")

    print("\n🧭 Instrucciones:")
    for i, paso in enumerate(path["instructions"]):
        texto = paso["text"]
        paso_km = paso["distance"] / 1000
        paso_mi = paso_km / 1.61
        print(f"{i+1}. {texto} ({paso_km:.2f} km / {paso_mi:.2f} mi)")

def mostrar_aereo(origen, destino, coords_orig, coords_dest):
    distancia = distancia_aerea(*coords_orig, *coords_dest)
    millas = distancia / 1.61
    velocidad = 800  # km/h
    duracion_horas = distancia / velocidad
    hrs = int(duracion_horas)
    mins = int((duracion_horas - hrs) * 60)

    print(f"\n✈️ Desde: {origen}")
    print(f"🛬 Hasta: {destino}")
    print(f"📏 Distancia aérea: {distancia:.2f} km / {millas:.2f} mi")
    print(f"⏱️ Tiempo estimado de vuelo: {hrs}h {mins}m")
    print(f"📝 Narrativa: El vuelo desde {origen} a {destino} cubrirá {distancia:.1f} km en {hrs}h {mins}m.")

def seleccionar_transporte():
    print("\n🚗 Seleccione medio de transporte:")
    print("1 - Automóvil")
    print("2 - Bicicleta")
    print("3 - Avión")
    print("Escriba 's' para salir.")
    eleccion = input("Opción: ").strip().lower()
    if eleccion == 's':
        return None
    opciones = {"1": "car", "2": "bike", "3": "plane"}
    if eleccion not in opciones:
        print("⚠️ Opción inválida. Se usará 'car'.")
    return opciones.get(eleccion, "car")

def main():
    print("\n🌎 Calculador de viajes entre ciudades de Chile y Perú")
    while True:
        medio = seleccionar_transporte()
        if not medio:
            break

        origen_ciudad = input("\nCiudad de Origen (Chile): ").strip()
        if origen_ciudad.lower() == 's':
            break
        origen = geocodificar(origen_ciudad)
        if not origen:
            continue

        destino_ciudad = input("Ciudad de Destino (Perú): ").strip()
        if destino_ciudad.lower() == 's':
            break
        destino = geocodificar(destino_ciudad)
        if not destino:
            continue

        if medio == "plane":
            mostrar_aereo(origen[2], destino[2], (origen[0], origen[1]), (destino[0], destino[1]))
        else:
            datos_ruta = ruta_terrestre(origen, destino, medio)
            if datos_ruta:
                mostrar_terrestre(datos_ruta, origen[2], destino[2], medio)

if __name__ == "__main__":
    main()



