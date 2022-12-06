"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

# Importaciones ---------------------------------------------------------

import config as cf
from DISClib.DataStructures import mapentry as me
import DISClib.ADT.graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from math import *
from prettytable import PrettyTable
from DISClib.Algorithms.Graphs import dijsktra, bfs
from DISClib.ADT import stack
from operator import itemgetter
import sys
assert cf
"""
cycles.DirectedCycle()
cycles.hasCycle()
dfo.dfsVertex()
dfs.pathTo()
dfs.hasPathTo
dijsktra.
bfs.BreadhtFisrtSearch()
"""
sys.setrecursionlimit(10**6)

# Construcción de modelo -------------------------------------------------

def inicializar_modelo() -> dict:

    """ 
        Inicializa el analyzer y sus estructuras de datos.
    """

    modelo = {
        "grafo": None,
        "paradas": None,
        "paradas_exclusivas": None,
        "paradas_compartidas": None, 
        "rutas": None,
        "rutas_unicas": None
    }
    
    modelo["grafo"] = gr.newGraph(
        datastructure='ADJ_LIST',
        directed=True,
        size=14000,
        comparefunction=None
    )

    modelo["paradas"] = mp.newMap(
        numelements=14000,
        maptype='PROBING',
        comparefunction=None
        )

    modelo["rutas"] = mp.newMap(
        numelements=14000,
        maptype='PROBING',
        comparefunction=None
        )

    modelo["paradas_exclusivas"] = mp.newMap(
        numelements=14000,
        maptype='PROBING',
        comparefunction=None
        )

    modelo["paradas_compartidas"] = mp.newMap(
        numelements=14000,
        maptype='PROBING',
        comparefunction=None
        )

    modelo["rutas_unicas"] = mp.newMap(
        numelements=14000,
        maptype='PROBING',
        comparefunction=None
        )
        
    return modelo

# Funcion para agregar informacion al modelo -----------------------------

def asignar_modelo(modelo: dict, archivo_paradas: str, archivo_rutas: str) -> dict:

    grafo = modelo["grafo"]
    paradas_dict = modelo["paradas"]
    rutas_dict = modelo["rutas"]
    paradas_exclusivas = modelo["paradas_exclusivas"]
    paradas_compartidas = modelo["paradas_compartidas"]
    rutas_unicas = modelo["rutas_unicas"]

    paradas_archivo = open(archivo_paradas, "r", encoding="utf-8")
    registro =  paradas_archivo.readline().replace("\n", "").split(",")
    registro =  paradas_archivo.readline().replace("\n", "").split(",")
    while len(registro) > 1:
        code = registro[0]
        bus_stop = registro[4]
        if not mp.contains(rutas_unicas, bus_stop):
            rutas_unicas = mp.put(rutas_unicas, bus_stop, registro)
        bus_stop_numero = (bus_stop.replace(" ", "").split("-"))[1]
        nombre_parada = code + "-" + bus_stop_numero
        paradas_dict = asignar_parada(paradas_dict, registro, nombre_parada)
        grafo = crear_vertice(grafo, nombre_parada)
        if registro[7] == "S":
            if not mp.contains(paradas_compartidas, code):
                paradas_compartidas = mp.put(paradas_compartidas, code, registro)
            nombre_parada = "T-"+code
            paradas_dict = asignar_parada(paradas_dict, registro, "T-"+code)
            grafo = crear_vertice(grafo, nombre_parada)
        else:
            if not mp.contains(paradas_exclusivas, code):
                paradas_exclusivas = mp.put(paradas_exclusivas, code, registro)
        registro =  paradas_archivo.readline().replace("\n", "").split(",")
    paradas_archivo.close()

    rutas_archivo = open(archivo_rutas, "r", encoding="utf-8")
    registro =  rutas_archivo.readline().replace("\n", "").split(",")
    registro =  rutas_archivo.readline().replace("\n", "").split(",")
    while len(registro) > 1:
        code = registro[0]
        bus_stop = registro[1]
        bus_stop_numero = (bus_stop.replace(" ", "").split("-"))[1]
        nombre_vertice_partida = code + "-" + bus_stop_numero
        code = registro[2]
        nombre_vertice_llegada = code + "-" + bus_stop_numero
        if gr.containsVertex(grafo, "T-"+code):
            grafo = crear_arco(grafo, nombre_vertice_partida, "T-"+code, haversine(paradas_dict, nombre_vertice_partida, "T-"+code))
            grafo = crear_arco(grafo, "T-"+code, nombre_vertice_llegada, haversine(paradas_dict, "T-"+code, nombre_vertice_llegada))
        rutas_dict = asignar_ruta(rutas_dict, registro, nombre_vertice_partida)
        rutas_dict = asignar_ruta(rutas_dict, registro, nombre_vertice_llegada)
        grafo = crear_arco(grafo, nombre_vertice_partida, nombre_vertice_llegada, haversine(paradas_dict, nombre_vertice_partida, nombre_vertice_llegada))
        registro =  rutas_archivo.readline().replace("\n", "").split(",")
    rutas_archivo.close()

    modelo["grafo"] = grafo
    modelo["paradas"] = paradas_dict
    modelo["rutas"] = rutas_dict
    modelo["paradas_exclusivas"] = paradas_exclusivas
    modelo["paradas_comprtidas"] = paradas_compartidas
    modelo["rutas_unicas"] = rutas_unicas

    return modelo

# Funciones de consulta -------------------------------------------------

def grafo_informacion(modelo: dict):
    
    rutas = mp.keySet(modelo["rutas_unicas"])

    print("\nTotal de rutas de bus disponibles: " + str(gr.numEdges(modelo["grafo"])) + ".")
    print("Total de estaciones exclusivas: " + str(mp.size(modelo["paradas_exclusivas"])) + ".")
    print("Total de estaciones compartidas: " + str(mp.size(modelo["paradas_compartidas"])) + ".")
    print("Total de rutas utilizadas en todas las rutas: " + str(lt.size(rutas)) + ".")

    longitud_maxima = 0
    latitud_maxima = 0
    paradas_codigos = mp.keySet(modelo["paradas_exclusivas"])

    for parada_codigo in lt.iterator(paradas_codigos):
        parada = me.getValue(mp.get(modelo["paradas_exclusivas"], parada_codigo))
        parada_longitud = float(parada[2])
        parada_latitud = float(parada[3])
        if parada_longitud > longitud_maxima:
            longitud_maxima = parada_longitud
        if parada_latitud > latitud_maxima:
            latitud_maxima = parada_latitud

    paradas_codigos = mp.keySet(modelo["paradas_compartidas"])

    for parada_codigo in lt.iterator(paradas_codigos):
        parada = me.getValue(mp.get(modelo["paradas_compartidas"], parada_codigo))
        parada_longitud = float(parada[2])
        parada_latitud = float(parada[3])
        if parada_longitud > longitud_maxima:
            longitud_maxima = parada_longitud
        if parada_latitud > latitud_maxima:
            latitud_maxima = parada_latitud

    longitud_minima = longitud_maxima
    latitud_minima = latitud_maxima

    paradas_codigos = mp.keySet(modelo["paradas_exclusivas"])

    for parada_codigo in lt.iterator(paradas_codigos):
        parada = me.getValue(mp.get(modelo["paradas_exclusivas"], parada_codigo))
        parada_longitud = float(parada[2])
        parada_latitud = float(parada[3])
        if parada_longitud < longitud_minima:
            longitud_minima = parada_longitud
        if parada_latitud < latitud_minima:
            latitud_minima = parada_latitud

    paradas_codigos = mp.keySet(modelo["paradas_compartidas"])

    for parada_codigo in lt.iterator(paradas_codigos):
        parada = me.getValue(mp.get(modelo["paradas_compartidas"], parada_codigo))
        parada_longitud = float(parada[2])
        parada_latitud = float(parada[3])
        if parada_longitud < longitud_minima:
            longitud_minima = parada_longitud
        if parada_latitud < latitud_minima:
            latitud_minima = parada_latitud

    print("Longitud minima del area cubierta por la red de buses: " + str(longitud_minima) + ".")
    print("Longitud maxima del area cubierta por la red de buses: " + str(longitud_maxima) + ".")
    print("Latitud minima del area cubierta por la red de buses: " + str(latitud_minima) + ".")
    print("Latitud maxima del area cubierta por la red de buses: " + str(latitud_maxima) + ".")

    paradas = gr.vertices(modelo["grafo"])
    paradas_tabla = PrettyTable(["Identificacion", "Latitud", "Longitud", "Numero de estaciones adyacentes"])
    for posicion in range(1, 6):
        parada_codigo = lt.getElement(paradas, posicion)
        parada = me.getValue(mp.get(modelo["paradas"], parada_codigo))
        paradas_tabla.add_row([parada_codigo, parada[3], parada[2], lt.size(gr.adjacents(modelo["grafo"], parada_codigo))])
    for posicion in range(lt.size(paradas)-6, lt.size(paradas)-1):
        parada_codigo = lt.getElement(paradas, posicion)
        parada = me.getValue(mp.get(modelo["paradas"], parada_codigo))
        paradas_tabla.add_row([parada_codigo, parada[3], parada[2], lt.size(gr.adjacents(modelo["grafo"], parada_codigo))])
    print("Primeras y ultiimas 5 estaciones registradas en el grafo:")
    print(paradas_tabla)

def req_1(modelo: dict, code_id_1: str, code_id_2: str):

    grafo = modelo["grafo"]
    paradas_dict = modelo["paradas"]
    caminos = bfs.BreadhtFisrtSearch(grafo, code_id_1)
    if bfs.hasPathTo(caminos, code_id_2):
        camino = bfs.pathTo(caminos, code_id_2)
        distancia = 0
        numero_transbordos = 0
        estaciones = PrettyTable(["Origen", "Destino", "Distancia"])
        geolocalizaciones = []
        estaciones_list = []
        numero_estaciones = stack.size(camino)
        while stack.size(camino) > 0:
            numero_estaciones = stack.size(camino)
            estacion_codigo = stack.pop(camino)
            if estacion_codigo[0] == "T":
                numero_transbordos += 1
            estacion_info = me.getValue(mp.get(paradas_dict, estacion_codigo))
            estaciones_list.append((estacion_codigo, estacion_info))
            geolocalizaciones.append((float(estacion_info[2]), float(estacion_info[3])))
        for pos in range(0, len(estaciones_list)):
            if pos+1 == len(estaciones_list):
                distancia_tramo = haversine(paradas_dict, estaciones_list[pos][0], code_id_2)
                distancia += distancia_tramo
                estaciones.add_row([estaciones_list[pos][0], code_id_2, str(distancia_tramo) + " km"])
            else:
                distancia_tramo = haversine(paradas_dict, estaciones_list[pos][0], estaciones_list[pos+1][0])
                distancia += distancia_tramo
                estaciones.add_row([estaciones_list[pos][0], estaciones_list[pos+1][0], str(distancia_tramo) + " km"])
        print("\nDistancia total de recorrido: " + str(distancia) + " km.")
        print("Total de estaciones que contiene el camino: " + str(numero_estaciones) + ".")
        print("Total de transbordos que contiene la ruta: " + str(numero_transbordos) + ".")
        print("Estaciones de la ruta:")
        print(estaciones)

    else:
        print("\nNo existe ruta entre ambas estaciones.")

    return (distancia, numero_estaciones, numero_transbordos, estaciones)

def req_2(modelo: dict, code_id_1: str, code_id_2: str):

    grafo = modelo["grafo"]
    caminos = dijsktra.Dijkstra(grafo, code_id_1)
    camino = dijsktra.pathTo(caminos, code_id_2)
    distancia = 0
    numero_estaciones = 0
    numero_transbordos = 0
    estaciones = PrettyTable(["Origen", "Destino", "Distancia"])
    if camino is None:
        print("\nNo existe ruta entre ambas estaciones.")
    else:
        numero_estaciones = stack.size(camino)
        while stack.size(camino) > 0:
            estacion = stack.pop(camino)
            distancia += estacion['weight']
            if estacion['vertexB'][0] == "T":
                numero_transbordos += 1
            estaciones.add_row([estacion['vertexA'], estacion['vertexB'], str(estacion['weight']) + " km"])
    
        print("\nDistancia total de recorrido: " + str(distancia) + " km.")
        print("Total de estaciones que contiene el camino: " + str(numero_estaciones) + ".")
        print("Total de transbordos que contiene la ruta: " + str(numero_transbordos) + ".")
        print("Estaciones de la ruta:")
        print(estaciones)

def req_3(modelo:dict):

    grafo = modelo["grafo"]
    vertices_lista = gr.vertices(grafo)
    vertices_conexiones_cantidad = {}
    for vertice in lt.iterator(vertices_lista):
        vertices_conexiones_cantidad[vertice] =  lt.size(gr.adjacents(grafo, vertice))
    vertices_conexiones_cantidad = dict(sorted(vertices_conexiones_cantidad.items(), key=itemgetter(1)))

    vertices = list(vertices_conexiones_cantidad.keys())
    table = PrettyTable(["Component", "Componentes conectados", "Primeras y ultimas 3 componentes conectadas"])
    for pos in range(1,6):
        conectadas = gr.adjacents(grafo, vertices[-pos])
        conectadas_codigos = ""
        for i in range(0,3):
            conectadas_codigo = str(lt.getElement(conectadas, i))
            conectadas_codigos += conectadas_codigo + "\n"
        for i in range(lt.size(conectadas)-4,lt.size(conectadas)-1):
            conectadas_codigo = str(lt.getElement(conectadas, i))
            conectadas_codigos += conectadas_codigo + "\n"
        table.add_row([vertices[-pos], vertices_conexiones_cantidad[vertices[-pos]], conectadas_codigos])
    print("\nEl total de componentes conectados en el grafo es: " + str(lt.size(vertices_lista)) + ".")
    print(table)

def req_4(modelo:dict, lon_origen:float, lat_origen:float, lon_destino:float, lat_destino:float):
    
    estaciones_origen = {}
    estaciones_destino = {}
    for estacion in lt.iterator(mp.keySet(modelo["paradas"])):
        if estacion[0] != "T":
            estacion_info = me.getValue(mp.get(modelo["paradas"], estacion))
            estaciones_origen[estacion] = haversine_2(lon_origen, lat_origen, float(estacion_info[2]), float(estacion_info[3]))
            estaciones_destino[estacion] = haversine_2(lon_destino, lat_destino, float(estacion_info[2]), float(estacion_info[3]))
    estaciones_origen = dict(sorted(estaciones_origen.items(), key=itemgetter(1)))
    estaciones_destino = dict(sorted(estaciones_destino.items(), key=itemgetter(1)))

    estacion_origen = (list(estaciones_origen.keys()))[0]
    estacion_destino = (list(estaciones_destino.keys()))[0]
        
    print("\nLa distancia entre la localización de origen y la estación de bus más cercana es de: " + str(estaciones_origen[estacion_origen]) + " km.")
    print("La distancia entre la estación destino más cercana y la localización destino es de: " + str(estaciones_destino[estacion_destino]) + " km.")
    req_2(modelo, estacion_origen, estacion_destino)

def req_5(modelo: dict, code_id_origen: str, cantidad_conexiones: int, cantidad_elementos: int):

    paradas_dict = modelo["paradas"]
    paradas_list = mp.keySet(paradas_dict)
    paradas_alcanzables = []
    contador = 0
    for parada_destino in lt.iterator(paradas_list):
        if parada_destino[0] != "T" and parada_destino != code_id_origen:
            camino_data = req_1_return(modelo, code_id_origen, parada_destino)
            if camino_data[1] <= cantidad_conexiones and camino_data[1] != -1:
                destino_data = me.getValue(mp.get(paradas_dict, parada_destino))
                tupla = (parada_destino, (destino_data[3], destino_data[2]), camino_data[0])
                paradas_alcanzables.append(tupla)
                contador += 1
                if contador == cantidad_elementos:
                    break
    tabla = PrettyTable(["Identificador", "Geolocalizacion", "Distancia del origen a la estacion"])
    for parada in paradas_alcanzables:
        tabla.add_row([parada[0], parada[1], str(parada[2]) + " km"])
    print(tabla)
        


# Funciones auxiliares --------------------------------------------------

def crear_vertice(grafo, nombre_parada: str):

    if not gr.containsVertex(grafo, nombre_parada):
        gr.insertVertex(grafo, nombre_parada)

    return grafo

def crear_arco(grafo, nombre_vertice_partida: str, nombre_vertice_llegada:str, peso: float):
    gr.addEdge(grafo, nombre_vertice_partida, nombre_vertice_llegada, peso)
    return grafo

def asignar_parada(paradas, parada: list, nombre_parada:str):
    paradas = mp.put(paradas, nombre_parada, parada)
    return paradas

def asignar_ruta(rutas, ruta: list, nombre_ruta:str):
    rutas = mp.put(rutas, nombre_ruta, ruta)
    return rutas

def haversine(paradas_dict, nombre_parada_1:str, nombre_parada_2:str): 

    lon_1 = me.getValue(mp.get(paradas_dict, nombre_parada_1))[2]
    lat_1 = me.getValue(mp.get(paradas_dict, nombre_parada_1))[3]
    lon_2 = me.getValue(mp.get(paradas_dict, nombre_parada_2))[2]
    lat_2 = me.getValue(mp.get(paradas_dict, nombre_parada_2))[3]

    lat_1 = float(lat_1)
    lon_1 = float(lon_1)
    lat_2 = float(lat_2)
    lon_2 = float(lon_2)
    r = 6372.8 
    d_lat = radians(lat_2 - lat_1)
    d_lon = radians(lon_2 - lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    a = sin(d_lat/2)**2 + cos(lat_1)*cos(lat_2)*sin(d_lon/2)**2
    c = 2*asin(sqrt(a)) 

    return r * c

def haversine_2(lon_1: float, lat_1: float, lon_2: float, lat_2: float): 

    lat_1 = float(lat_1)
    lon_1 = float(lon_1)
    lat_2 = float(lat_2)
    lon_2 = float(lon_2)
    r = 6372.8 
    d_lat = radians(lat_2 - lat_1)
    d_lon = radians(lon_2 - lon_1)
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    a = sin(d_lat/2)**2 + cos(lat_1)*cos(lat_2)*sin(d_lon/2)**2
    c = 2*asin(sqrt(a)) 

    return r * c

def req_1_return(modelo: dict, code_id_1: str, code_id_2: str) -> tuple:

    grafo = modelo["grafo"]
    paradas_dict = modelo["paradas"]
    caminos = bfs.BreadhtFisrtSearch(grafo, code_id_1)
    distancia = -1
    numero_estaciones = -1
    if bfs.hasPathTo(caminos, code_id_2):
        camino = bfs.pathTo(caminos, code_id_2)
        distancia = 0
        estaciones_list = []
        numero_estaciones = stack.size(camino)
        while stack.size(camino) > 0:
            numero_estaciones = stack.size(camino)
            estacion_codigo = stack.pop(camino)
            estacion_info = me.getValue(mp.get(paradas_dict, estacion_codigo))
            estaciones_list.append((estacion_codigo, estacion_info))
        for pos in range(0, len(estaciones_list)):
            if pos+1 == len(estaciones_list):
                distancia_tramo = haversine(paradas_dict, estaciones_list[pos][0], code_id_2)
                distancia += distancia_tramo
            else:
                distancia_tramo = haversine(paradas_dict, estaciones_list[pos][0], estaciones_list[pos+1][0])
                distancia += distancia_tramo

    return (distancia, numero_estaciones)

#datos = asignar_modelo(inicializar_modelo(), "./Data/paradas.csv", "./Data/rutas.csv")
#req_5(datos, "1772-88", 1, 5)
#grafo_informacion(asignar_modelo(inicializar_modelo(), "./Data/paradas.csv", "./Data/rutas.csv"))