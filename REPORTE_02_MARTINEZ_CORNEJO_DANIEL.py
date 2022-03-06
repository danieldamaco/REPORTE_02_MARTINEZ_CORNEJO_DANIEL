#!/usr/bin/env python
# coding: utf-8

# # Inicio de código

# In[1]:


import pandas as pd


# In[2]:


pd.options.display.float_format = '${:,.2f}'.format


# In[3]:


df = pd.read_csv('/Users/danielmartinez/Desktop/EMTECH/Proyecto_final_2/synergy_logistics_database.csv')
df


# # Cambio de tipos de variable

# In[4]:


df.dtypes


# In[5]:


df['total_value'] = df['total_value'].astype('float')


# In[6]:


df[['direction', 'origin', 'destination', 'product', 'transport_mode', 'company_name']] = df[['direction', 'origin', 'destination', 'product', 'transport_mode', 'company_name']].astype('category')


# In[7]:


df['year'] = pd.to_datetime(
    df['year'],
    errors='coerce',
    format = '%m/%d/%Y %H:%M:%S %p'
)


# In[8]:


df['date'] = pd.to_datetime(
    df['date'],
    errors='coerce',
    format = '%m/%d/%Y %H:%M:%S %p'
)


# In[9]:


df.dtypes


# # Resolución de problemas

# ## Opción 1) Rutas de importación y exportación. 
# 
# * Synergy logistics está considerando la posibilidad de enfocar sus esfuerzos en las 10 rutas más demandadas. Acorde a los flujos de importación y exportación, ¿cuáles son esas 10 rutas? 
# 
# * ¿le conviene implementar esa estrategia? ¿porqué?

# In[10]:


"""* Agrupamiento varibales 'origin' y 'destination', contando el número de apariciones.
* Ordenamiento descendente de veces contadas. 
"""
df_grouped = df.groupby(['origin', 'destination']).count()
df_grouped_sorted = df_grouped.sort_values('product', ascending=False)


# In[11]:


"""Creación de dataframe con top 10 rutas.
Creación de archivo Excel con dataframe df_top_10_routes.
"""
df_top_10_routes = df_grouped_sorted['register_id'].head(10)
df_top_10_routes.to_excel(r'/Users/danielmartinez/Desktop/EMTECH/Proyecto_final_2/excel/Top_10_routes.xlsx')
df_top_10_routes


# In[12]:


"""* Agrupamiento varibales 'origin' y 'destination', sumando los datos.
* Ordenamiento descendente de ganancia. 
"""
df_grouped = df.groupby(['origin', 'destination']).sum()
df_grouped_sorted = df_grouped.sort_values('total_value', ascending=False)


# In[13]:


"""Creación de dataframe con top 10 rutas por ganancia.
Creación de archivo Excel con dataframe df_top_10_routes_earn.
"""
df_top_10_routes_earn = df_grouped_sorted['total_value'].head(10)
df_top_10_routes_earn.to_excel(r'/Users/danielmartinez/Desktop/EMTECH/Proyecto_final_2/excel/Top_10_routes_earn.xlsx')
df_top_10_routes_earn


# ## Opción 2) Medio de transporte utilizado. 
# + ¿Cuáles son los 3 medios de transporte más importantes para Synergy logistics considerando el valor de las importaciones y exportaciones? 
# + ¿Cuál es medio de transporte que podrían reducir?

# In[14]:


"""Agrupamiento por variable transport_mode, sumando los valores y ordenándolos de forma descendente segíun variable
total_value
"""
df_most_used_transport = df.groupby(['transport_mode']).sum().sort_values('total_value', ascending=False)
df_most_used_transport


# In[15]:


"""Exportar el dataframe df_most_used_transport a archivo Excel"""
df_most_used_transport.to_excel(r'/Users/danielmartinez/Desktop/EMTECH/Proyecto_final_2/excel/Most_used_transport.xlsx')


# ## Opción 3) Valor total de importaciones y exportaciones. 
# 
# Si Synergy Logistics quisiera enfocarse en los países que le generan el 80% del valor de las exportaciones e importaciones 
# * ¿en qué grupo de países debería enfocar sus esfuerzos?

# In[16]:


"""Agrupamiento por variables origin, destination y direction, sumando 
y ordenando de forma descendente según la variable total_value"""
df_countries = df.groupby(['origin', 'destination', 'direction']).sum()
df_countries_sorted = df_countries.sort_values('total_value', ascending=False)


# In[17]:


"""Creación de columan cumsum que genera la suma acumulada de la variable total_value
"""
df_countries_sorted['cumsum'] = df_countries_sorted['total_value'].cumsum()


# In[18]:


"""Creación de la variable percentage que genera el porcentaje acumulado de las ganancias por ruta.
"""
df_countries_sorted['percentage'] = df_countries_sorted['cumsum'] / df_countries_sorted['total_value'].sum() * 100


# In[19]:


"""Cambio de forma de expresar los decimales."""
pd.options.display.float_format = '{:,.2f}%'.format
df_80 = df_countries_sorted[['percentage', 'total_value']].head(62).reset_index()
df_80


# In[20]:


df_80[['origin','destination']]


# In[21]:


df_80_destination = df_80.groupby('destination').sum()
df_80_destination = df_80_destination.drop(['percentage'], axis=1).sort_values('total_value', ascending=False).reset_index()
df_80_destination['cumsum'] = df_80_destination['total_value'].cumsum()
df_80_destination['cumul_percentage'] = df_80_destination['cumsum'] / df_80_destination['total_value'].sum() * 100
df_80_destination.rename(columns={'destination':'countries'}, inplace=True)
df_80_destination.head(12).to_excel(r'/Users/danielmartinez/Desktop/EMTECH/Proyecto_final_2/excel/Top_countries_destination.xlsx')
df_80_destination


# In[22]:


df_80_origin = df_80.groupby('origin').sum()
df_80_origin = df_80_origin.drop(['percentage'], axis=1).sort_values('total_value', ascending=False).reset_index()
df_80_origin['cumsum'] = df_80_origin['total_value'].cumsum()
df_80_origin['cumul_percentage'] = df_80_origin['cumsum'] / df_80_origin['total_value'].sum() * 100
df_80_origin.rename(columns={'origin':'countries'}, inplace=True)
df_80_origin.head(7).to_excel(r'/Users/danielmartinez/Desktop/EMTECH/Proyecto_final_2/excel/Top_countries_origin.xlsx')
df_80_origin
