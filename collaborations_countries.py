# -*- coding: utf-8 -*-
"""
@author: Isis
"""
#Importar librerias
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import re

#Cargar datos

countries = open("unCountriesData.txt" , 'r') #Cargar archivo de texto que contiene todos los paises reconocidos por la ONU
country_list = [line.split(',') for line in countries.readlines()] #Convertirlo a lista

df = pd.read_excel('savedrecs.xls') #Cargar la base de datos (archivo de excel)
direc = df["Addresses"] #Guardar solo la columna de las direcciones
df_paises = pd.DataFrame() #Crear un data frame vacio

n = len(country_list[0]) #Longitud de la lista de paises

#Llenar df_paises, cada fila contiene los paises en una address 
for i in range(len(direc)):
    #Crear el nombre de la columna
    string = 'Pais '
    tracker = 1
    
    #Toma cada direccion para analizar individualmente
    address = direc[i]
    
    #Encuentra los paises y los guarda en el df
    for j in range (n):
        x = re.search(country_list[0][j], address) #Encuentra el pais
        
        #Para que no se detenga la busqueda despues del el primer match
        while x: 
            new_column = string + str(tracker) #Crea una columna
            df_paises.at[i, new_column] = x.group() #Guarda el pais encontrado
            address = address.replace(x.group(), "", 1) #Quita el pais de la address
            x = re.search(country_list[0][j], address) #Vuelve a buscar un pais
            tracker += 1 #Para que el siguiente pais se guarde en otra columna
                

lista = [] #Crear una lista vacia

#Llenar la lista con solo los paises que aparecen en el df
for col in df_paises.columns:
    for pais in df_paises[col]:
        if pais not in lista:
            lista.append(pais)
    
n1 = len(lista) #Longitud de la lista

#crear una matriz vacia
adjacency_matrix = np.zeros((n1,n1), dtype=int) #Matriz adyacente vacia

columns = df_paises.columns #Guardar las columnas

#Iteran sobre toda la matriz
for i in range(df_paises.shape[0]):
    for j, column in enumerate(columns):
        if df_paises.at[i,col] != None: 
            if j < len(columns) - 1: 
                #Busca los paises que colaboran y encuentra sus indices
                x = lista.index(df_paises.at[i, columns[j]])  
                y = lista.index(df_paises.at[i, columns[j + 1]])
                #Suma 1 cada vez que hay una colaboracion
                adjacency_matrix[x][y] += 1
                adjacency_matrix[y][x] += 1
          
#Suma cada fila
suma_rows = np.sum(adjacency_matrix, axis = 1)

#Normalizar la matriz, divide cada valor entre la suma de su fila
normalized_matrix = adjacency_matrix / suma_rows[:, np.newaxis]

#Crear un graph de nx con la matriz adyacente normalizada
G = nx.from_numpy_matrix(normalized_matrix, parallel_edges = True, create_using = nx.MultiGraph())

#Graficar 
np.random.seed(42) #Para que el grafico sea igual cada vez 
pos = nx.spring_layout(G)  
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', width=1.5)

plt.show()

