from datetime import datetime

TRClist = ["ADD","AUT","CIB","CYD","FPH","IEE","IMM"]

def calcular_semestres(desde_año):
    año_actual = datetime.now().year
    semestres = ((año_actual - desde_año) * 2) + 1
    return semestres

def obtener_equiv_semestre(mallaEE, mallaMI, equiv, semestre):
    mallaMI = mallaMI[(mallaMI.semestre <= semestre) & (mallaMI.semestre != 0) & (mallaMI.semestre <= 10)].copy()
    creditosIMI = mallaMI.creditos.sum()
    listaMI = mallaMI.codigo.to_list()
    equivOK = []
    equivfil = equiv.copy()
    equivfil["codigoMI"] = equivfil["codigoMI"].str.split(";",expand=False)    

    for _,fila in equivfil.iterrows():
        presente = True
        if str(fila.codigoMI) != "nan":
            for codi in fila.codigoMI:
                presente = presente & (codi in listaMI)
            if presente: equivOK.append(fila.codigoEE)

    equivfinal = equiv[equiv.codigoEE.isin(equivOK)].reset_index(drop=True)
    equivfinal = equivfinal.merge(mallaEE[["codigo", "creditos", "nombre", "area"]], left_on="codigoEE", right_on="codigo", how="left").drop(columns=["codigo"])
    creditosTRC = equivfinal[equivfinal.area.isin(TRClist)].creditos.sum()
    creditosINS = creditosTRC + equivfinal[equivfinal.area == "INS"].creditos.sum()
    creditosAER = creditosTRC + equivfinal[equivfinal.area == "AER"].creditos.sum()
    creditosSCF = creditosTRC + equivfinal[equivfinal.area == "SCF"].creditos.sum()

    return creditosIMI, creditosTRC, creditosINS, creditosAER, creditosSCF, equivfinal

def obtener_equiv_lista(mallaEE, mallaMI, equiv, lista):
    listaMI = lista
    mallaMI = mallaMI[mallaMI.codigo.isin(listaMI)]
    creditosIMI = mallaMI.creditos.sum()
    equivOK = []
    equivfil = equiv.copy()
    equivfil["codigoMI"] = equivfil["codigoMI"].str.split(";",expand=False)    

    for _,fila in equivfil.iterrows():
        presente = True
        if str(fila.codigoMI) != "nan":
            for codi in fila.codigoMI:
                presente = presente & (codi in listaMI)
            if presente: equivOK.append(fila.codigoEE)

    equivfinal = equiv[equiv.codigoEE.isin(equivOK)].reset_index(drop=True)
    equivfinal = equivfinal.merge(mallaEE[["codigo", "creditos", "nombre", "area"]], left_on="codigoEE", right_on="codigo", how="left").drop(columns=["codigo"])
    creditosTRC = equivfinal[equivfinal.area.isin(TRClist)].creditos.sum()
    creditosINS = creditosTRC + equivfinal[equivfinal.area == "INS"].creditos.sum()
    creditosAER = creditosTRC + equivfinal[equivfinal.area == "AER"].creditos.sum()
    creditosSCF = creditosTRC + equivfinal[equivfinal.area == "SCF"].creditos.sum()

    return creditosIMI, creditosTRC, creditosINS, creditosAER, creditosSCF, equivfinal
    
def calcular_porcentajes(creditosIMI, creditosTRC, creditosINS, creditosAER, creditosSCF):
    totcreditosIMI = 177
    totcreditosTRC = 135
    totcreditosENF = 180
    porcIMI = round(creditosIMI/totcreditosIMI,3)
    porcTRC = round(creditosTRC/totcreditosTRC,3)
    porcINS = round(creditosINS/totcreditosENF,3)
    porcAER = round(creditosAER/totcreditosENF,3)
    porcSCF = round(creditosSCF/totcreditosENF,3)

    return porcIMI, porcTRC, porcINS, porcAER, porcSCF

def aprobadas_carne(carnet, estudiantes):
    estudiante = estudiantes[estudiantes["Carnet"]==carnet].copy()
    nombre = estudiante.Nombre.item()
    estudiante.drop(columns=["Año de Ingreso al TEC","Carnet","Nombre"],inplace=True)
    cursos = estudiante.transpose().dropna().index.tolist()
    return cursos, nombre


