"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
import DISClib.ADT.graph as gr
from DISClib.ADT import map as mp
assert cf
import sys

sys.setrecursionlimit(10**6)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido\n")
    print("1. Cargar información en el catálogo.")
    print("2. Buscar un camino posible entre dos estaciones.")
    print("3. Buscar el camino con menos estaciones entre dos estaciones.")
    print("4. Reconocer los componentes conectados de la Red de rutas de bus.")
    print("0. Salir del programa.\n")

modelo = None
continuar = True

"""
Menu principal
"""
while True:

    printMenu()
    inputs = input('Seleccione una opción para continuar: ')

    if int(inputs[0]) == 1:

        archivo_paradas = input('Ingrese el nombre del archivo de paradas: ')
        archivo_paradas = "./Data/" + archivo_paradas
        archivo_rutas = input('Ingrese el nombre del archivo de rutas: ')
        archivo_rutas = "./Data/" + archivo_rutas
        modelo = controller.cargar_datos(controller.inicalizar_modelo(), archivo_paradas, archivo_rutas)
        controller.grafo_informacion(modelo)

    elif int(inputs[0]) == 2:
        code_id_1 = input('Ingrese el CODE-ID de la estación de partida: ')
        code_id_2 = input('Ingrese el CODE-ID de la estación de destino: ')
        controller.req_1(modelo, code_id_1, code_id_2)

    elif int(inputs[0]) == 3:
        code_id_1 = input('Ingrese el CODE-ID de la estación de partida: ')
        code_id_2 = input('Ingrese el CODE-ID de la estación de destino: ')
        controller.req_2(modelo, code_id_1, code_id_2)

    elif int(inputs[0]) == 4:
        controller.req_3(modelo)


    elif int(inputs[0]) == 0:
        sys.exit(0)

sys.exit(0)
