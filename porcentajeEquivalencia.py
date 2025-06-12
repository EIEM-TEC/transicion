from datetime import datetime
import pandas as pd

mallaMI = pd.read_csv("MI1313.csv")
equiv = pd.read_csv("cursos_equiv.csv")

def calcular_semestres():
    desde_año = int(input("Digite el año de ingreso:"))
    año_actual = datetime.now().year
    semestres = ((año_actual - desde_año) * 2)+1
    return semestres

def obtener_coincidencias_individuales(mallaMI, equiv):
    semestre = calcular_semestres()
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

    totOK = listafinal.shape[0]
    totMI = len(listaMI)

    #print(len(listaMI))
    #print(listafinal)
    #print(listafinal.shape[0])

    return totMI, totOK, listafinal
    

def calcular_porcentajes(totMI,totOK):
    cursosMI = 67
    cursosEE = 58
    porcentajeMI = totMI*100/cursosMI
    porcentajeEE = totOK*100/cursosEE
    print("El porcentaje de cursos de MI es:",porcentajeMI,"%")
    print("El porcentaje de cursos de EE es:",porcentajeEE,"%")
    return porcentajeEE, porcentajeMI

totMI, totOK, listafinal = obtener_coincidencias_individuales(
    mallaMI,
    equiv,
)
calcular_porcentajes(totMI,totOK)


