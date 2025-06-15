import funciones as fun
import pandas as pd

mallaEE = pd.read_csv("malla_EE.csv")
mallaMI = pd.read_csv("malla_MI.csv")
equiv = pd.read_csv("equivalencias.csv")


años = [2025,2024,2023,2022,2021]

tabla = pd.DataFrame(index=años, columns=[  
                                "creditosIMI",
                                "creditosTRC",
                                "creditosINS",
                                "creditosAER",
                                "creditosSCF",
                                "porcIMI",
                                "porcTRC",
                                "porcINS",
                                "porcAER",
                                "porcSCF"
                            ])
tabla.index.name = 'año'



for año in años:
    semestre = fun.calcular_semestres(año) + 1
    tabla.loc[año,"creditosIMI"],\
    tabla.loc[año,"creditosTRC"],\
    tabla.loc[año,"creditosINS"],\
    tabla.loc[año,"creditosAER"],\
    tabla.loc[año,"creditosSCF"],\
    equivfinal=\
    fun.obtener_equiv_semestre(
        mallaEE,
        mallaMI,
        equiv,
        semestre,
    )
    tabla.loc[año,"porcIMI"],\
    tabla.loc[año,"porcTRC"],\
    tabla.loc[año,"porcINS"],\
    tabla.loc[año,"porcAER"],\
    tabla.loc[año,"porcSCF"]=\
    fun.calcular_porcentajes(
        tabla.loc[año,"creditosIMI"],
        tabla.loc[año,"creditosTRC"],
        tabla.loc[año,"creditosINS"],
        tabla.loc[año,"creditosAER"],
        tabla.loc[año,"creditosSCF"],
    )
    equivfinal.to_csv(f"tabla_{año}.csv",index=False)
    
tabla.to_csv("tabla_años.csv")