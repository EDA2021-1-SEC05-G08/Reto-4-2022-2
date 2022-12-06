﻿"""
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

datos = asignar_modelo(inicializar_modelo(), "./Data/paradas.csv", "./Data/rutas.csv")
req_1(datos, "358-119", "356-119")
#grafo_informacion(asignar_modelo(inicializar_modelo(), "./Data/paradas.csv", "./Data/rutas.csv"))