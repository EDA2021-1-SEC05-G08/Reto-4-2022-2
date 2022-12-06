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
 """

import config as cf
import model
import sys

sys.setrecursionlimit(10**6)

def inicalizar_modelo() -> dict:
    return model.inicializar_modelo()

def cargar_datos(modelo:dict, archivo_paradas: str, archivo_rutas: str) -> dict:
    return model.asignar_modelo(modelo, archivo_paradas, archivo_rutas)

def grafo_informacion(modelo: dict):
    model.grafo_informacion(modelo)

def req_1(modelo: dict, code_id_1: str, code_id_2: str):
    model.req_1(modelo, code_id_1, code_id_2)

def req_2(modelo: dict, code_id_1: str, code_id_2: str):
    model.req_2(modelo, code_id_1, code_id_2)

def req_3(modelo: dict):
    model.req_3(modelo)

def req_4(modelo:dict, lon_origen:float, lat_origen:float, lon_destino:float, lat_destino:float):
    model.req_4(modelo, lon_origen, lat_origen, lon_destino, lat_destino)