import pandas as pd
import os

# Ruta al archivo CSV
data_path = os.path.join('..', 'data', 'raw', 'supply_chain_data.csv')

# Leer CSV
df = pd.read_csv(data_path)

# Información básica
print("=" * 50)
print("EXPLORACIÓN INICIAL DEL DATASET")
print("=" * 50)
print(f"\n📊 Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"\n📋 Columnas:\n{df.columns.tolist()}")
print(f"\n🔍 Primeras 5 filas:")
print(df.head())
print(f"\n📈 Info del dataset:")
print(df.info())
print(f"\n📊 Estadísticas descriptivas:")
print(df.describe())
print(f"\n❓ Valores nulos por columna:")
print(df.isnull().sum())
print(f"\n✅ Tipos de productos únicos: {df['Product type'].nunique()}")
print(df['Product type'].value_counts())