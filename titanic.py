#Generar un DataFrame con los datos del archivo.
import pandas as pd
datos_titanic = pd.read_csv('titanic.csv')
#print(datos_titanic)

#Mostrar por pantalla las dimensiones del DataFrame, 
# el número de datos que contiene, 
# los nombres de sus columnas y filas, 
# los  tipos de datos de las columnas, 
# las 10 primeras filas y las 10 últimas filas.
#print(datos_titanic.info())
#print(datos_titanic.describe)
#print(datos_titanic.columns)
#print(datos_titanic.shape)
#Mostrar por pantalla los datos del pasajero con identificador 148.
pasajero_148=datos_titanic.loc[147]
#print(pasajero_148)

#Mostrar por pantalla las filas pares del DataFrame.
filas_par= datos_titanic[datos_titanic.index % 2 ==0]
#print(filas_par)

# Filtrar pasajeros de primera clase y ordenar por nombre
pasajeros_primera = datos_titanic[datos_titanic['Pclass'] == 1].sort_values('Name')

# Mostrar solo la columna 'Name' (nombres ordenados)
#['Name'].to_string(index=False) 
# imprime únicamente la columna de nombres, excluyendo el índice del DataFrame
#print(pasajeros_primera['Name'].to_string(index=False))

# Calcular el número total de pasajeros
total_pasajeros = len(datos_titanic)

# Contar cuántos murieron (Survived = 0) y sobrevivieron (Survived = 1)
#Obtenidos en la base de datos
muertos = len(datos_titanic[datos_titanic['Survived'] == 0])
sobrevivientes = len(datos_titanic[datos_titanic['Survived'] == 1])

porcentaje_muertos = (muertos / total_pasajeros) * 100
porcentaje_sobrevivientes = (sobrevivientes / total_pasajeros) * 100

#print(f"Porcentaje de personas que murieron: {porcentaje_muertos:.2f}%")
#print(f"Porcentaje de personas que sobrevivieron: {porcentaje_sobrevivientes:.2f}%")

#Mostrar por pantalla el porcentaje de personas que sobrevivieron en cada clase.
sobrevivientes_clases = []
for clase in [1, 2, 3]:
    # Filtrar pasajeros por clase
    pasajeros = datos_titanic[datos_titanic['Pclass'] == clase]
    # Calcular porcentaje de supervivencia
    porcentaje = (pasajeros['Survived'].sum() / len(pasajeros)) * 100
    sobrevivientes_clases.append(f"Clase {clase}: {porcentaje:.2f}%")

#print("Porcentaje de sobrevivientes por clase:")
#print('\n'.join(sobrevivientes_clases))

#Eliminar del DataFrame los pasajeros con edad desconocida.
# Eliminar filas donde 'Age' es NaN (edad desconocida)
datos_titanic_limpios = datos_titanic.dropna(subset=['Age'])

# Mostrar el número de filas antes y después para verificar
#print(f"Filas originales: {len(datos_titanic)}")
#print(f"Filas después de eliminar edades desconocidas: {len(datos_titanic_limpios)}")



#Mostrar por pantalla la edad media de las mujeres que viajaban en cada clase.
# Filtrar solo mujeres y agrupar por clase para calcular la edad media
#
edad_media_mujeres_por_clase = datos_titanic[datos_titanic['Sex'] == 'female'].groupby('Pclass')['Age'].mean()
# Mostrar el resultado con formato claro
#print("Edad media de las mujeres por clase:")
#.round(2) redondea el resultado a 2 decimales
#.to_string() evita se muestren notaciones cientificas
#print(edad_media_mujeres_por_clase)

# Añadir una nueva columna booleana para ver si el pasajero era menor de edad o no.
datos_titanic['Menor_de_edad'] = datos_titanic['Age'] < 18
#print(datos_titanic[['Name', 'Age', 'Menor_de_edad']].head())
#Esta linea nos permite saber cuantos de los pasajeros en total son menores de edad.
#print(f"Número de menores de edad: {datos_titanic['Menor_de_edad'].sum()}")

#Mostrar por pantalla el porcentaje de menores y mayores de edad que sobrevivieron en cada clase.
datos_titanic['Menor_de_edad'] = datos_titanic['Age'] < 18
porcentaje_supervivencia = (
    datos_titanic
    .groupby(['Pclass', 'Menor_de_edad'])['Survived']
    .mean()  
    .mul(100) 
    .round(2)  
    .reset_index()  # Convierte a DataFrame
)

porcentaje_supervivencia.columns = ['Clase', 'Menor_de_edad', 'Porcentaje_Sobrevivieron']
porcentaje_supervivencia['Menor_de_edad'] = porcentaje_supervivencia['Menor_de_edad'].map(
    {True: 'Menor (Age < 18)', False: 'Mayor (Age ≥ 18)'})

print(porcentaje_supervivencia.to_string(index=False))