﻿"""
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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido\n")
    print("1. Cargar información en el catálogo.")
    print("0. Salir del programa\n")

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
        archivo_rutas = input('Ingrese el nombre del archivo de paradas: ')
        archivo_rutas = "./Data/" + archivo_rutas
        modelo = controller.cargar_datos(controller.inicalizar_modelo(), archivo_paradas, archivo_rutas)
        print("\nTotal de rutas de bus disponibles: " + str(gr.numEdges(modelo["grafo"])) + ".")

    elif int(inputs[0]) == 0:
        sys.exit(0)

sys.exit(0)