from datetime import datetime
import pandas as pd

mallaEE = pd.read_csv("cursos_malla.csv")
mallaMI = pd.read_csv("MI1313.csv")
equiv = pd.read_csv("cursos_equiv.csv")


def calcular_semestres(desde_año):
    año_actual = datetime.now().year
    semestres = ((año_actual - desde_año) * 2) + 1
    return semestres

def obtener_coincidencias_individuales(mallaEE, mallaMI, equiv, semestre):
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
    listafinal = listafinal.merge(mallaEE[["codigo", "nombre"]], left_on="codigoEE", right_on="codigo", how="left").drop(columns=["codigo"])
    listafinal.to_csv("equivEstudiante.csv",index=False)

    totOK = listafinal.shape[0]
    totMI = len(listaMI)

    #print(len(listaMI))
    print(listafinal)
    #print(listafinal.shape[0])

    return totMI, totOK, listafinal
    
semestre = 8

def calcular_porcentajes(totMI,totOK):
    cursosMI = 67
    cursosEE = 58
    porcentajeMI = round(totMI*100/cursosMI,1)
    porcentajeEE = round(totOK*100/cursosEE,1)
    print("El porcentaje de cursos de MI es:",porcentajeMI,"%")
    print("El porcentaje de cursos de EE es:",porcentajeEE,"%")
    return porcentajeEE, porcentajeMI

totMI, totOK, listafinal = obtener_coincidencias_individuales(
    mallaEE,
    mallaMI,
    equiv,
    semestre,
)
calcular_porcentajes(totMI,totOK)


