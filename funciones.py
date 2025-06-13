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
        #print(f"{fila.codigoEE},{fila.codigoMI}")
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
    porcIMI = round(creditosIMI*100/totcreditosIMI,1)
    porcTRC = round(creditosTRC*100/totcreditosTRC,1)
    porcINS = round(creditosINS*100/totcreditosENF,1)
    porcAER = round(creditosAER*100/totcreditosENF,1)
    porcSCF = round(creditosSCF*100/totcreditosENF,1)

    return porcIMI, porcTRC, porcINS, porcAER, porcSCF


