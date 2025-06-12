from datetime import datetime
import pandas as pd

mallaMI = pd.read_csv("MI1313.csv")
equiv = pd.read_csv("cursos_equiv.csv")

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

def obtener_coincidencias_individuales(semestre, mallaMI, equiv):
    """
    Analiza cada códigoIM por separado, incluso si están en la misma fila separados por ';'.
    Guarda coincidencias individuales en un CSV.
    """
    mallaMI = mallaMI[(mallaMI.semestre <= semestre) & (mallaMI.semestre != 0)].copy()
    listaMI = mallaMI.codigo.to_list()
    equivOK = []
    equivfil = equiv.copy()
    equivfil["codigoMI"] = equivfil["codigoMI"].str.split(";",expand=False)    

    for _,fila in equivfil.iterrows():
        
        presente = True
        #print(f"{fila.codigoEE},{fila.codigoMI}")
        if str(fila.codigoMI) != "nan":
            for codi in fila.codigoMI:
                presente = presente & (codi in listaMI)
            if presente: equivOK.append(fila.codigoEE)

    listafinal = equiv[equiv.codigoEE.isin(equivOK)].reset_index(drop=True)
    listafinal.to_csv("hola.csv",index=False)

    print(len(listaMI))
    print(listafinal.shape[0])

semestres = 1

cantidad = obtener_coincidencias_individuales(
    semestres,
    mallaMI,
    equiv,
)



