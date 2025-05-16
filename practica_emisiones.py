import pandas as pd
#Vamos a leer nuestros archivos en el DataFrame
emisiones_2016 = pd.read_csv('emisiones-2016.csv', sep=';')
emisiones_2017 = pd.read_csv('emisiones-2017.csv', sep=';')
emisiones_2018 = pd.read_csv('emisiones-2018.csv', sep=';')
emisiones_2019 = pd.read_csv('emisiones-2019.csv', sep=';')

emisiones = pd.concat([emisiones_2016, emisiones_2017, emisiones_2018, emisiones_2019], ignore_index=True)
#print(emisiones.columns)

# Filtrar columnas deseadas
columnas_deseadas = ['ESTACION', 'MAGNITUD', 'ANO', 'MES'] + [col for col in emisiones.columns if col.startswith('D') and col[1:].isdigit()]
emisiones_filtradas = emisiones[columnas_deseadas]
#print(emisiones_filtradas)

id_vars = ['ESTACION', 'MAGNITUD', 'ANO', 'MES']

#Derretir (melt) el DataFrame
emisiones_reestructurado = pd.melt(
    emisiones,
    id_vars=id_vars,
    value_vars=[f'D{i:02d}' for i in range(1, 32)],
    var_name='DIA',
    value_name='VALOR'
)
#Limpiar y formatear la columna DIA (opcional, quita la 'D' inicial)
emisiones_reestructurado['DIA'] = emisiones_reestructurado['DIA'].str.replace('D', '').astype(int)

#Ordenar el DataFrame (opcional)
emisiones_reestructurado = emisiones_reestructurado.sort_values(['ESTACION', 'MAGNITUD', 'ANO', 'MES', 'DIA'])

#Mostrar el resultado
#print(emisiones_reestructurado.head())

emisiones_reestructurado['FECHA'] = pd.to_datetime(
    emisiones_reestructurado['ANO'].astype(str) + '-' + 
    emisiones_reestructurado['MES'].astype(str) + '-' + 
    emisiones_reestructurado['DIA'].astype(str),
    format='%Y-%m-%d',  # Especifica el formato de entrada
    errors='coerce'     # Convierte fechas inválidas en NaT
)

# 2. Eliminar filas con fechas inválidas (opcional)
emisiones_reestructurado = emisiones_reestructurado.dropna(subset=['FECHA'])

#Verificar el resultado
#print(emisiones_reestructurado[['ESTACION', 'MAGNITUD', 'FECHA', 'VALOR']].head())

import numpy as np

# Suponiendo que ya tienes el DataFrame con la columna 'FECHA' creada anteriormente
# Eliminar filas con fechas no válidas
emisiones_reestructurado = emisiones_reestructurado[~np.isnat(emisiones_reestructurado['FECHA'])]

# Ordenar por estación y fecha
emisiones_reestructurado = emisiones_reestructurado.sort_values(['ESTACION', 'FECHA'])

# Resetear el índice (opcional)
emisiones_reestructurado = emisiones_reestructurado.reset_index(drop=True)

# Mostrar el resultado final
#print("\nDataFrame limpio y ordenado:")
#print(emisiones_reestructurado[['ESTACION', 'MAGNITUD', 'FECHA', 'VALOR']].head())


# Mostrar estaciones únicas
estaciones_unicas = emisiones_reestructurado['ESTACION'].unique()
print("\nEstaciones disponibles:")
print(sorted(estaciones_unicas))

# Mostrar contaminantes (magnitudes) únicos
contaminantes_unicos = emisiones_reestructurado['MAGNITUD'].unique()
print("\nContaminantes disponibles:")
print(sorted(contaminantes_unicos))