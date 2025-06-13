import funciones as fun
import pandas as pd

año = int(input("\nIngresar año: "))
semestre = fun.calcular_semestres(año)

print(f"\nCalculo realizado para {semestre} semestre(s)\n")

mallaEE = pd.read_csv("malla_EE.csv")
mallaMI = pd.read_csv("malla_MI.csv")
equiv = pd.read_csv("equivalencias.csv")

creditosIMI,\
creditosTRC,\
creditosINS,\
creditosAER,\
creditosSCF,\
equivfinal=\
fun.obtener_equiv_semestre(
    mallaEE,
    mallaMI,
    equiv,
    semestre,
)



porcIMI,\
porcTRC,\
porcINS,\
porcAER,\
porcSCF=\
fun.calcular_porcentajes(
    creditosIMI,
    creditosTRC,
    creditosINS,
    creditosAER,
    creditosSCF,
)

print(equivfinal)

print(f"\nPara una persona estudiante con carné {año}:")
print(f"Créditos en IMI: {creditosIMI}, porcentaje: {porcIMI} %")
print(f"Créditos en TRC: {creditosTRC}, porcentaje: {porcTRC} %")
print(f"Créditos en INS: {creditosINS}, porcentaje: {porcINS} %")
print(f"Créditos en AER: {creditosAER}, porcentaje: {porcAER} %")
print(f"Créditos en SCF: {creditosSCF}, porcentaje: {porcSCF} %\n")

