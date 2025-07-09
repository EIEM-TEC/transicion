import funciones as fun
import pandas as pd
from pylatex import Document, Package, Command,\
    simple_page_number,\
    TikZ, TikZOptions
from pylatex.utils import NoEscape, bold, italic



cursos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv")
#cursos = pd.read_csv("cursos_malla.csv")
mallaMI = pd.read_csv("malla_MI.csv")
cursos['sevesreq'] = cursos['creditos'] * 0.0
cursos['sevreq'] = cursos['creditos'] * 0.0
equiv = pd.read_csv("equivalencias.csv")
estudiantes = pd.read_csv("datos\\2021_2025.csv")

areas = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/areas.csv")

TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]
INS = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS"]
AER = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","AER"]
SCF = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","SCF"]

#carnet = 2021023053 #mare
#carnet = 2023234861 #angie
carnet = 2022055783 # kendall

nombre, estudiante = fun.por_carnet(carnet,estudiantes,cursos,mallaMI,equiv)
print(estudiante)
lista_aprob_est = estudiante["codigoEE"].unique()

cursosest = cursos
cursosest["aprobadas"] = cursosest["codigo"].apply(lambda x: "A" if x in lista_aprob_est else "P")


fun.generar_malla_carnet(cursosest,carnet)


# por_carnet(carnetangi,est)
