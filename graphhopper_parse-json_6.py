import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "ce5ff66d-549f-43fa-8cb7-a0b6d071c874"

line = "=" * 50


def geocoding(location, key):
    while location == "":
        location = input("[Enter] para ingresar la ubicación nuevamente: ")
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key, "locale": "es"})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = (json_data["hits"][0]["point"]["lat"])
        lng = (json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print(f"API URL de Geocoding para {new_loc} (Tipo de ubicación: {value})\n{url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print(f"Geocode API status: {str(json_status)}\nError message: {json_data['message']}")

    return json_status, lat, lng, new_loc


while True:
    loc1 = input("Ciudad de Origen: ")
    if loc1 == "salir" or loc1 == "s":
        break
    orig = geocoding(loc1, key)
    print(orig)
    loc2 = input("Ciudad de Destino: ")
    if loc2 == "salir" or loc2 == "s":
        break
    dest = geocoding(loc2, key)
    print(line)
    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={str(orig[1])}%2C{str(orig[2])}"
        dp = f"&point={str(dest[1])}%2C{str(dest[2])}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print(line)
        print(f"Dirección desde {orig[3]}; con Destino a {dest[3]}")
        print(line)
        if paths_status == 200:
            kilometros = (paths_data["paths"][0]["distance"]) / 1000
            segundos = int(paths_data["paths"][0]["time"] / 1000 % 60)
            minutos = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            horas = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia a recorrer: {0:.2f} kilómetros".format(kilometros))
            print("Duración del Viaje: {0:02d}:{1:02d}:{2:02d}".format(horas, minutos, segundos))
            print(line)
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km )".format(path, distance / 1000, distance / 1000 / 1.61))
            print(line)
                                                                                                                                                                                                                                                                
