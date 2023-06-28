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
        
df_paises = df_paises.fillna("none")


lista = [] #Crear una lista vacia

#Llenar la lista con solo los paises que aparecen en el df
for col in df_paises.columns:
    for pais in df_paises[col]:
        if pais not in lista and pais != "none":
            lista.append(pais)

n1 = len(lista) #Longitud de la lista

#crear una matriz vacia
adjacency_matrix = np.zeros((n1,n1), dtype=int) #Matriz adyacente vacia

columns = df_paises.columns #Guardar las columnas

#Iteran sobre toda la matriz
for i in range(df_paises.shape[0]):
    for j in range(len(columns)):
        for k in range(len(columns)-1):
            if k < len(columns) - 1: 
                if df_paises.at[i, columns[j]] != "none" and df_paises.at[i, columns[k]] != "none" :
            
                    #Busca los paises que colaboran y encuentra sus indices
                    x = lista.index(df_paises.at[i, columns[j]])  
                    y = lista.index(df_paises.at[i, columns[k]])
                    #Suma 1 cada vez que hay una colaboracion
                    adjacency_matrix[x][y] += 1
                    adjacency_matrix[y][x] += 1

      
#Suma cada fila
suma_rows = np.sum(adjacency_matrix, axis = 1)
suma_rows = np.where(suma_rows == 0, 1, suma_rows) #replazar los ceros por 1 para que no haya error por dividir entre 0
      

#Normalizar la matriz, divide cada valor entre la suma de su fila
normalized_matrix = adjacency_matrix / suma_rows[:, np.newaxis]

#Crear un graph de nx con la matriz adyacente normalizada
G = nx.from_numpy_matrix(normalized_matrix, parallel_edges = True, create_using = nx.MultiGraph())
 

#Crear el diccionario
mapping = {}
for i in range(len(lista)):
    mapping[i] = lista[i]
    
G = nx.relabel_nodes(G, mapping)

node_sizes = []
for i in range(normalized_matrix.shape[0]):
    node_sizes.append(suma_rows[i]*20)

#Graficar 
np.random.seed(5) #Para que el grafico sea igual cada vez 
#pos = nx.kamada_kawai_layout(G) 
#pos = nx.spiral_layout(G) 
pos = nx.random_layout(G) 

pos[' Peru'] = [0.99331, 0.664565]
pos[' India'] = [0.83331, 0.504565]
pos[' Bulgaria'] = [0.83331, 0.704565]
pos[' Mexico'] = [0.98146874, 0.3989448]
pos[' New Zealand'] = [0.5999292,0.26581913]
pos[' Canada'] = [0.7,0.1]
pos[' Indonesia'] = [0.5,0.1]
pos[' Brazil'] = [0.4,0.2]
pos[' Spain'] = [0.7,0.45]
pos[' France'] = [0.1,0.1]
pos[' Italy'] = [0.3,0.4]
pos[' Thailand'] = [0.001,0.3]
pos[' Japan'] = [0.15,0.45]
pos[' Bangladesh'] = [0.25,0.66]
pos[' Turkey'] = [0.45,0.9]
pos[' USA'] = [0.002,0.98]
pos[' Poland'] = [0.3,0.1]

nx.draw(G, pos, node_size= node_sizes , with_labels=True, node_color='lightblue', edge_color='gray', width=1.7)
plt.savefig("analisis_biblio.png")
#plt.show()