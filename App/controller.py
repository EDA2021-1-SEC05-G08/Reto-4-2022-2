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