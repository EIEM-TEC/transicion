from datetime import datetime
import pandas as pd

def calcular_semestres(desde_año):
    año_actual = datetime.now().year
    semestres = ((año_actual - desde_año) * 2)+1
    return semestres

def contar_filas_y_listar_codigos_por_semestre(ruta_csv, semestres_maximos):
    try:
        df = pd.read_csv(ruta_csv)

        # Verificamos que existan las columnas necesarias
        if 'semestre' not in df.columns or 'codigo' not in df.columns:
            raise ValueError("El archivo debe tener columnas 'semestre' y 'codigo'.")

        # Asegurarse de que los valores sean numéricos
        df['semestre'] = pd.to_numeric(df['semestre'], errors='coerce')

        # Filtrar filas con semestre > 0 y <= semestres_maximos
        filtro = (df['semestre'] > 0) & (df['semestre'] <= semestres_maximos)
        df_filtrado = df[filtro]

        cantidad = df_filtrado.shape[0]
        codigos = df_filtrado['codigo'].tolist()

        return cantidad, codigos

    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return 0, []

def obtener_coincidencias_completas(codigos_validos, equivalencias_csv):
    """
    Revisa fila por fila en cursos_equiv.csv si todos los codigos de codigoIM (separados por ';')
    están en codigos_validos (lista de MI1313.csv).
    Retorna la cantidad de coincidencias y la lista de codigoEE que cumplen la condición.
    """
    df_equiv = pd.read_csv(equivalencias_csv)
    coincidencias = []

    for _, fila in df_equiv.iterrows():
        codigos_im_fila = str(fila['codigoIM']).split(';')
        codigos_im_fila = [c.strip() for c in codigos_im_fila]

        # Verificar que TODOS los códigos estén en codigos_validos
        if all(codigo in codigos_validos for codigo in codigos_im_fila):
            coincidencias.append(fila['codigoEE'])

    return len(coincidencias), coincidencias



semestres = int(input("Ingresa la cantidad de semestres: "))
_, codigos_validos = contar_filas_y_listar_codigos_por_semestre("MI1313.csv", semestres)

cantidad, lista_coincidencias = obtener_coincidencias_completas(codigos_validos, "cursos_equiv.csv")

print(f"Cantidad de coincidencias: {cantidad}")
print("Lista de codigoEE con coincidencia completa:")
for i, codigo_ee in enumerate(lista_coincidencias, start=1):
    print(f"{i}. {codigo_ee}")


