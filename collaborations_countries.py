# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 18:42:20 2023

@author: yanet
"""
import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import re

#lista de paises
countries = open("unCountriesData.txt" , 'r')
country_list = [line.split(',') for line in countries.readlines()]

# crear el df
df = pd.read_excel('savedrecs.xls')

#guardar solo la columna de las direcciones
direc = df["Addresses"] 

# agregarle columnas vacias al df

df_paises = pd.DataFrame()

n = len(country_list[0])

for i in range(len(direc)):
    string = 'Pais '
    tracker = 1
    address = direc[i]
    
    for j in range (n):
        
        x = re.search(country_list[0][j], address)
        
        while x: 
            new_column = string + str(tracker)
            df_paises.at[i, new_column] = x.group()
            address = address.replace(x.group(), "", 1)
            x = re.search(country_list[0][j], address)
            tracker += 1
                

lista = []

for col in df_paises.columns:
    for pais in df_paises[col]:
        if pais not in lista:
            lista.append(pais)
    
n1 = len(lista)

#crear una matriz vacia
adjacency_matrix = np.zeros((n1,n1), dtype=int)

iteration =  df_paises['Pais 1'].tolist()

columns = df_paises.columns

for i in range(len(iteration)):
    for j, column in enumerate(columns):
        if df_paises.at[i,col] != None:
            if j < len(columns) - 1: 
                x = lista.index(df_paises.at[i, columns[j]])  
                y = lista.index(df_paises.at[i, columns[j + 1]])
                adjacency_matrix[x][y] += 1
                adjacency_matrix[y][x] += 1
          
#Normalizar 
suma_rows = np.sum(adjacency_matrix, axis = 1)

normalized_matrix = adjacency_matrix / suma_rows[:, np.newaxis]

G = nx.from_numpy_matrix(normalized_matrix, parallel_edges = True, create_using = nx.MultiGraph())

print(G.nodes())
print(G.edges())

pos = nx.spring_layout(G)  
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', width=1.5)

plt.show()

