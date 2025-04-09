#!/usr/bin/env python
# coding: utf-8

# In[59]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[60]:


df=pd.read_csv("/Users/apare/Documents/SF_WR_19_24.csv", index_col=None) #Aqui creo mi df, en base a mi csv
##, usando como columna 1, mis encabezados.
## este CSV esta hecho de las estadisticas ofensivas en los juegos contra los Seahawks de los años 2019-2024 de los SF, 49ers.


# In[61]:


df #Aqui 


# In[62]:


print(df.columns)
print(df.shape)
print(df.head())
print(df.info())
#Vamos a revisar nuestro df, checando un poco de sus propiedades.


# In[63]:


# Extraer las últimas 3 letras y guardarlas en una nueva columna
df['Posicion'] = df['Nombre'].str[-2:]  # Tomar las últimas dos letras (para "TE", "QB", etc.)

# Eliminar las últimas 3 letras (el nombre se queda solo)
df['Nombre'] = df['Nombre'].str[:-3]


# In[64]:


##Tengo los valores de Targets y Recepciones por jugador 
##Pero me gustaria saber el porcentaje de recepciones por jugador , creare una nueva columna
##dividiendo las recepciones sobre los targets 
df["Porcentaje de recepciones"]= df["Recepciones"] / df ["Targets"] * 100
df["Porcentaje de recepciones"]=df["Porcentaje de recepciones"].round(2)
df


# In[65]:


#algo que me llamo la atencion son las columnas de Fumbles , Yardas por juego y fumbles recuperados
#vere si tienen algun valor diferente de cero 
def sumar_columnas(df, columnas):
    # Crear un diccionario para almacenar las sumas de cada columna
    suma_columnas = {}
    # Iterar a través de la lista de columnas y calcular la suma
    for columna in columnas:
        if columna in df.columns:
            suma_columnas[columna] = df[columna].sum()
        else:
            suma_columnas[columna] = 'Columna no encontrada'
    
    return suma_columnas


# In[66]:


## Cree una funcion que le aplica la suma total a las columnas seleccionadas.
##Para asi ver si es que tienen valores diferentes de cero
columnas = ['Fumbles','Yardas por juego','Fumbles recuperados'] 
sumar_columnas(df,columnas)


# In[67]:


#La suma de las columnas totales me dio cero para los casos de Fumbles, Yardas por Juego, Fumbles recuperados para 
#tener un df, mas limpio pasare a quitar esas columnas, no tiene caso tenerlas.
df = df.drop(['Fumbles','Yardas por juego','Fumbles recuperados'],axis=1)

#pude notar que hay guardias (G) y centros (C), que se encuentran en mi df, voy a eliminar las filas con esas posiciones
df = df[~df['Posicion'].isin([' C', ' G'])]


# In[68]:


### cambiare el nombre de Y por Año
df = df.rename(columns={'Y': 'Año'})


# In[69]:


#### reordenare la columna para que tenga sentido 
df = df [['Nombre','Posicion', 'Año', 'Recepciones', 'Targets','Porcentaje de recepciones', 'Yardas Recibidas', 'Promedio',
       'TD', 'LARGO', 'Grandes jugadas', 'Yardas despues de recepcion',
       'Recepcion de primer down']]


# # Ya tenemos el df limpio, y con posiciones relevantes en la ofensiva, primero vamos a ver la distribucion de posiciones en todos los años

# In[70]:


#usando seaborn ppodemos ver que de todos los años los WR son los que han tenido mas prescencia entre el roster de los 49ers
sns.countplot(x="Posicion",data=df)
plt.show()


# In[71]:


# Porcentaje de recepciones por posición
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='Posicion', y='Porcentaje de recepciones', palette='Set2')
plt.title('Porcentaje de Recepciones por Posición')
plt.xlabel('Posición')
plt.ylabel('Porcentaje de Recepciones')
plt.show()


# # Se me hizo interesante remarcar que en el periodo seleccionado los RB, tuvieran mejor porcentaje de recepciones que los WR, cuando de hecho se esperaria que fuera al reves. 

# In[72]:


# Distribución de Recepciones
plt.figure(figsize=(10, 6))
sns.histplot(df['Recepciones'], kde=True, color='skyblue')
plt.title('Distribución de Recepciones')
plt.xlabel('Recepciones')
plt.ylabel('Frecuencia')
plt.show()


# # Podemos inferir que el juego de los 49ers en estos años se centro mas en pases cortos, teninendo un pico en recepciones menores de 5 yardas, decrecen significativamente pases mayores a 25 yardas.

# In[73]:


plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Targets', y='Recepciones', hue='Posicion', palette='Set1')
plt.title('Relación entre Targets y Recepciones')
plt.xlabel('Targets')
plt.ylabel('Recepciones')
plt.legend(title='Posición')
plt.show()


# # Hay una relacion  lineal para dos posiciones, para los WR, y TE, mientras mas intentos de pase (Targets) tuvieron, mas recepciones completaron, esto igual nos puede indicar que se sienten mas comodos teniendo esas dos posiciones como preferencia para lanzarles pases.

# In[ ]:





# # Ahora que terminamos de ver un poco lo general, vamonos a lo individual

# In[74]:


#Vamos a revisar algunas estadisticas de dos de mis jugadores favoritos.
Samuel_19=df["Nombre"] == "Deebo Samuel Sr."
df[Samuel_19].plot(x="Año", y="Yardas Recibidas",kind="line")
plt.show()


# # Las Yardas Recibidas de Samuel (WR) tuvieron un pico grande en 2021, con +900 yardas , justo en el año en el que se acababa su contrato, para los años posteriores se mantuvo en promedio entre 400 y 500 yardas.

# In[75]:


Kittle_85=df["Nombre"] == "George Kittle"
df[Kittle_85].plot(x="Año", y="Yardas Recibidas",kind="line")
plt.show()


# # Para el caso de Kittle (TE), observamos que de 2020 en adelante tuvo un crecimiento en yardas recibidas, teniendo un crecimiento de +200 yardas en el año 2022 siendo este un maximo en su carrera.

# In[76]:


#TD por posicion y por año 
df_TD_Año = df.groupby(['Año','Posicion'])["Yardas Recibidas"].sum()
print(df_TD_Año)


# # Analizando por posicion y por año, la cantidad de Yardas Recibidas, tuvo una tendencia a aumentar apartir del 2020 para los WR, apartir de ese no bajaron de 1300 yardas. En comparacion que los TE, en las que no solo bajaron las yardas recibidas, si no que no han superado su maximo (609) en 2019.
# 

# In[58]:


# ahora para ver un poco mas dinamico el asunto me gustaria ver la info en POWERBI, entonces haremos el df, csv para alimentar
#directo powerbi con la informacion que tenemos

df.to_csv('jugadores_data.csv', index=False)


# # Podemos concluir que el plan para estos juegos se centro en lanzar a los WR, y TE, siendo estos dos grupos los mas targeteados y con mas recepciones, deje un poco de fuera las otras columnas para continuar el analisis utilizando PowerBi. 
# 
# # Gracias por su atencion!

# In[ ]:




