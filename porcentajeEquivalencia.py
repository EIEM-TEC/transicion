from datetime import datetime

def calcular_semestres(desde_año):
    año_actual = datetime.now().year
    semestres = ((año_actual - desde_año) * 2)+1
    return semestres

import pandas as pd

def contar_filas_y_listar_codigos_por_semestre(ruta_csv, semestres_maximos):
    try:
        df = pd.read_csv(ruta_csv)

        if 'semestre' not in df.columns or 'codigo' not in df.columns:
            raise ValueError("El archivo debe contener las columnas 'semestre' y 'codigo'.")

        df['semestre'] = pd.to_numeric(df['semestre'], errors='coerce')
        filtro = (df['semestre'] > 0) & (df['semestre'] <= semestres_maximos)
        df_filtrado = df[filtro]

        cantidad = df_filtrado.shape[0]
        codigos = df_filtrado['codigo'].tolist()

        return cantidad, codigos

    except Exception as e:
        print(f"Error leyendo '{ruta_csv}': {e}")
        return None, None

def buscar_coincidencias_con_todos_los_codigos(codigos_validos, equivalencias_csv):
    try:
        df_equiv = pd.read_csv(equivalencias_csv)

        if 'codigoIM' not in df_equiv.columns:
            raise ValueError("La columna 'codigoIM' no está en el archivo de equivalencias.")

        coincidencias = []

        for _, fila in df_equiv.iterrows():
            codigos_en_fila = str(fila['codigoIM']).split(';')
            codigos_en_fila = [c.strip() for c in codigos_en_fila]

            # Solo agregar si TODOS los códigos en la fila están en la lista de códigos válidos
            if all(codigo in codigos_validos for codigo in codigos_en_fila):
                coincidencias.append(fila)

        df_coincidencias = pd.DataFrame(coincidencias)

        return df_coincidencias

    except Exception as e:
        print(f"Error leyendo '{equivalencias_csv}': {e}")
        return pd.DataFrame()

# Ejemplo de uso
try:
    semestres_ingresados = int(input("Ingresa la cantidad de semestres: "))
    
    cantidad, codigos_filtrados = contar_filas_y_listar_codigos_por_semestre("MI1313.csv", semestres_ingresados)

    if cantidad is not None:
        print(f"\nCantidad de códigos válidos desde MI1313.csv: {cantidad}")
        df_resultado = buscar_coincidencias_con_todos_los_codigos(codigos_filtrados, "cursos_equiv.csv")

        print(f"\nSe encontraron {df_resultado.shape[0]} coincidencias (todos los códigos coinciden):")
        print(df_resultado)
except ValueError:
    print("Por favor, ingresa un número válido.")


