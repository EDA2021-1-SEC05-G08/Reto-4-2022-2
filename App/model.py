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
from math import *
assert cf

# Construcción de modelo -------------------------------------------------

def inicializar_modelo() -> dict:

    """ 
        Inicializa el analyzer y sus estructuras de datos.
    """

    modelo = {
        "grafo": None,
        "paradas": None,
        "rutas": None
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
        
    return modelo

# Funcion para agregar informacion al modelo -----------------------------

def asignar_modelo(modelo: dict, archivo_paradas: str, archivo_rutas: str) -> dict:

    grafo = modelo["grafo"]
    paradas_dict = modelo["paradas"]
    rutas_dict = modelo["rutas"]

    paradas_archivo = open(archivo_paradas, "r", encoding="utf-8")
    registro =  paradas_archivo.readline().replace("\n", "").split(",")
    registro =  paradas_archivo.readline().replace("\n", "").split(",")
    while len(registro) > 1:
        asignar_parada
        code = registro[0]
        bus_stop = registro[4]
        bus_stop_numero = (bus_stop.replace(" ", "").split("-"))[1]
        nombre_parada = code + "-" + bus_stop_numero
        paradas_dict = asignar_parada(paradas_dict, registro, nombre_parada)
        grafo = crear_vertice(grafo, nombre_parada)
        if registro[7] == "S":
            nombre_parada = "T-"+code
            paradas_dict = asignar_parada(paradas_dict, registro, "T-"+code)
            grafo = crear_vertice(grafo, nombre_parada)
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

    return modelo

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

