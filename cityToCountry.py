# -*- coding: utf-8 -*-
"""
Created on Sat May 27 08:37:43 2023

@author: yanet
"""

import pandas as pd
import re

#lista de paises
countries = open("unCountriesData.txt" , 'r')
country_list = [line.split(',') for line in countries.readlines()]

# crear el df
df = pd.read_excel('savedrecs.xls')

#guardar solo la columna de las direcciones
direc = df["Addresses"] 

# agregarle columnas vacias al df
df['Pais 1'] = None
df['Pais 2'] = None
df['Pais 3'] = None

for i in range(len(direc)):
    tracker = 1
    address = direc[i]
    
    for j in range (len(country_list[0])):
        x = re.search(country_list[0][j], address)
        if x != None:
            if tracker == 1:
                #print(x.group())
                df.at[i, 'Pais 1'] = x.group()
                tracker += 1
            elif tracker == 2:
                df.at[i, 'Pais 2'] = x.group()
                tracker += 1
            else:
                df.at[i, 'Pais 3'] = x.group()
                tracker += 1
           
"""
adjacency matrix
hacer array de los paises
poner numero de vees que se colaboro
networkx
network = matriz ad
nx.draw(network)
"""







