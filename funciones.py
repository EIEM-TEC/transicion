from datetime import datetime
import roman
from pylatex import Document, Package, Command, HorizontalSpace, TikZ, TikZOptions
from pylatex.utils import NoEscape, bold, italic
from pylatex.base_classes import Arguments
from pylatex.utils import NoEscape, bold, italic


TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]
INS = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS"]
AER = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","AER"]
SCF = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","SCF"]

def por_carnet(carnet,estudiantes,cursos,mallaMI,equiv):
    lista ,nombre= aprobadas_carne(carnet,estudiantes)
    creditosIMI,\
    creditosTRC,\
    creditosINS,\
    creditosAER,\
    creditosSCF,\
    equivfinal=\
    obtener_equiv_lista(
        cursos,
        mallaMI,
        equiv,
        lista,
    )
    porcIMI,\
    porcTRC,\
    porcINS,\
    porcAER,\
    porcSCF=\
    calcular_porcentajes(
        creditosIMI,
        creditosTRC,
        creditosINS,
        creditosAER,
        creditosSCF,
    )
    print(f"\nPara {nombre}:")
    print(f"Créditos en IMI: {creditosIMI}, porcentaje: {round(porcIMI*100,2)} %")
    print(f"Créditos en TRC: {creditosTRC}, porcentaje: {round(porcTRC*100,2)} %")
    print(f"Créditos en INS: {creditosINS}, porcentaje: {round(porcINS*100,2)} %")
    print(f"Créditos en AER: {creditosAER}, porcentaje: {round(porcAER*100,2)} %")
    print(f"Créditos en SCF: {creditosSCF}, porcentaje: {round(porcSCF*100,2)} %\n")
    return nombre, equivfinal

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
    creditosTRC = equivfinal[equivfinal.area.isin(TRC)].creditos.sum()
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
    creditosTRC = equivfinal[equivfinal.area.isin(TRC)].creditos.sum()
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

def number_to_ordinals(number_str):
    match number_str:
        case "1" | "3":
            number_str += r"\textsuperscript{er}"
        case "2":
            number_str += r"\textsuperscript{do}"
        case "4" | "5" | "6":
            number_str += r"\textsuperscript{to}"
        case "7" | "10":
            number_str += r"\textsuperscript{mo}"
        case "8":
            number_str += r"\textsuperscript{vo}"
        case "9":
            number_str += r"\textsuperscript{no}"
    return number_str 

def gen_list_porc(N):
    # Verificar que N esté entre 0 y 100
    if N < 0 or N > 100:
        raise ValueError("El número debe estar entre 0 y 100 inclusive.")
    
    # Generar la lista de números múltiplos de 10 hasta N
    lista_numeros = list(range(10, N + 1, 10))
    
    # Generar la lista de cadenas con el signo '%'
    lista_porcentajes = [f"{numero}%" for numero in lista_numeros]
    
    return lista_numeros, lista_porcentajes

def textcolor(size,vspace,color,bold,text,hspace="0"):
    dump = NoEscape(r"\par")
    if hspace!="0":
        dump += NoEscape(HorizontalSpace(hspace,star=True).dumps())
    dump += NoEscape(Command("fontsize",arguments=Arguments(size,vspace)).dumps())
    dump += NoEscape(Command("selectfont").dumps()) + NoEscape(" ")
    if bold==True:
        dump += NoEscape(Command("textbf", NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())).dumps())
    else:
        dump += NoEscape(Command("textcolor",arguments=Arguments(color,text)).dumps())
    return dump

def colocar_titulo(titulo,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"({round(57/2)},{round(4)})")
    dump += NoEscape(f"pic{{titulo={{{titulo},{color}}}}};")
    return dump

def colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila-0.5,2)})")
    dump += NoEscape(f"pic{{curso={{{codigo},{nombre},{round(horasteoria)},{round(horaspractica)},{round(creditos)},{color}}}}};")
    return dump

def colocar_semestre(semestre,sesgo,color,horasteoriasemestre,horaspracticasemestre,creditossemestre):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(0)})")
    if semestre == 0:
        dump += NoEscape(f"pic{{semestre={{{semestre},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    else:
        dump += NoEscape(f"pic{{semestre={{{roman.toRoman(semestre)},{color},{horasteoriasemestre},{horaspracticasemestre},{creditossemestre}}}}};")
    return dump

def colocar_arrowreq(semestre,sesgo,fila,sesgovert,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Stealth[length=3mm,width=2mm]}},{color},line width=0.5mm]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)-3.85,2)},{round(-4.2*fila-sesgovert,2)}) -- ")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)-2.03,2)},{round(-4.2*fila-sesgovert,2)});")
    return dump

def colocar_arrowreqs(semestre,sesgo,fila,dir,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[{color},line width=0.5mm]") 
    if dir == 1:
        dump += NoEscape(f"({round(6.87*(semestre-sesgo)-3.85,2)},{round(-4.2*fila-3.5,2)}) --++ (0.3,0) --++ (0,1.8)coordinate(inicio)")
    else:
        dump += NoEscape(f"({round(6.87*(semestre-sesgo)-3.85,2)},{round(-4.2*fila+2.5,2)}) --++ (0.3,0) --++ (0,-1.8)coordinate(inicio)")
    dump += NoEscape(r";")
    dump += NoEscape("\n")
    dump += NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Stealth[length=3mm,width=2mm]}},{color},line width=0.5mm]")
    dump += NoEscape(f"(inicio) --++ (1.55,0)")
    dump += NoEscape(r";")
    dump += NoEscape("\n")
    dump += NoEscape(r"\draw ")
    dump += NoEscape(f"[fill,{color}] ")
    dump += NoEscape(f"(inicio) circle (0.45mm)")
    dump += NoEscape(r";")
    return dump


def colocar_arrowcoreq(semestre,sesgo,fila,dir,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Stealth[length=3mm,width=2mm]}},{color},line width=0.5mm]")
    if dir == 1:
        dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila-3.08,2)}) --++ ")
        dump += NoEscape(f"(0,0.97);")
    if dir == -1:
        dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila+2.08,2)}) --++ ")
        dump += NoEscape(f"(0,-0.97);")        
    return dump

def colocar_diaesreq(semestre,sesgo,fila,sesgovert,num,color):#1.35 de largo
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Turned Square[open,length=4mm,line width=0.25mm,width=4mm]}},{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+3.02,2)},{round(-4.2*fila-sesgovert,2)}) --++ (1.35,0) ")
    dump += NoEscape(r"node[align=center,text width=4mm,xshift=-4.5mm]{\color{black}\fontsize{10pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{num}")
    dump += NoEscape(r"}};")                 
    return dump

def colocar_diareq(semestre,sesgo,fila,sesgovert,num,color):#1.35 de largo
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[{{Turned Square[open,length=4mm,line width=0.25mm,width=4mm]}}-,{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)-3.38,2)},{round(-4.2*fila-sesgovert,2)}) ")
    dump += NoEscape(r"node[align=center,text width=4mm,xshift=4.5mm]{\color{black}\fontsize{10pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{num}")
    dump += NoEscape(r"}}")  
    dump += NoEscape(f"--++ (1.35,0);")
    return dump

def colocar_triacoreq(semestre,sesgo,fila,num,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Triangle[reversed,open,length=3mm,line width=0.25mm,width=4mm]}},{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila+1.11,2)}) --++ ")
    dump += NoEscape(f"(0,0.94)")
    dump += NoEscape(r"node[align=center,text width=4mm,yshift=-2.5mm]{\color{black}\fontsize{10pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{num}")
    dump += NoEscape(r"}};")      
    return dump

def colocar_triaescoreq(semestre,sesgo,fila,num,color):
    dump = NoEscape(r"\draw ")
    dump += NoEscape(f"[-{{Triangle[open,length=3mm,line width=0.25mm,width=4mm]}},{color},line width=0.5mm,]")
    dump += NoEscape(f"({round(6.87*(semestre-sesgo)+0.5,2)},{round(-4.2*fila-2.11,2)}) --++ ")
    dump += NoEscape(f"(0,-0.94)")    
    dump += NoEscape(r"node[align=center,text width=4mm,yshift=4.5mm]{\color{black}\fontsize{10pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{num}")
    dump += NoEscape(r"}};")      
    return dump

def colocar_recreq(titulo1,titulo2,color):
    dump = NoEscape(r"\filldraw ")
    dump += NoEscape(f"[fill=white, draw=black]")
    dump += NoEscape(r"(30,1) ")
    dump += NoEscape(r" rectangle ") 
    dump += NoEscape(r" ++ (25,-40);")
    dump += NoEscape("\n")
    dump += NoEscape(r"\filldraw ")
    dump += NoEscape(f"[fill={color}, draw=black]")
    dump += NoEscape(r"(30,1) ")
    dump += NoEscape(r" rectangle ") 
    dump += NoEscape(r" ++ (25,-2) node[midway,align=center,text width=60mm]{\color{black}\fontsize{20pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{titulo1}")
    dump += NoEscape(r"}};") 
    dump += NoEscape("\n")
    dump += NoEscape(r"\filldraw ")
    dump += NoEscape(f"[fill={color}, draw=black]")
    dump += NoEscape(r"(30,-18) ")
    dump += NoEscape(r" rectangle ") 
    dump += NoEscape(r" ++ (25,-2) node[midway,align=center,text width=60mm]{\color{black}\fontsize{20pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{titulo2}")
    dump += NoEscape(r"}};") 
    return dump

def colocar_notasTC(textonota,sesgo):
    dump = NoEscape(r"\filldraw ")
    dump += NoEscape(r"[fill=white, draw=white]")
    dump += NoEscape(f"(25,{round(-39.8-sesgo*.8,2)})")
    dump += NoEscape(r" node[align=left,text width=490mm]{\color{black}\fontsize{16pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{sesgo}. {textonota}")
    dump += NoEscape(r"}};") 
    return dump

def colocar_notas(textonota,sesgo):
    dump = NoEscape(r"\filldraw ")
    dump += NoEscape(r"[fill=white, draw=white]")
    dump += NoEscape(f"(31,{round(-19-sesgo*2)})")
    dump += NoEscape(r" rectangle ") 
    dump += NoEscape(r" ++ (23,-2) node[midway,align=left,text width=220mm]{\color{black}\fontsize{16pt}{10pt}\selectfont \textbf{")
    dump += NoEscape(f"{sesgo}. {textonota}")
    dump += NoEscape(r"}};") 
    return dump

def malla_año(malla,cursos,sesgo,lista,titulo,rango,enf,año):
        reqcounter = 0
        malla.append(colocar_titulo(titulo,"lightgray"))
        if enf:
            malla.append(colocar_recreq("Electivas","Notas","lightgray"))
            malla.append(colocar_notas("Cursos del tronco común en color blanco",1))
            malla.append(colocar_notas("Debe escogerse 2 de las 9 electivas posibles para cursarlas en el décimo semestre",2))
            malla.append(colocar_notas("Debe realizarse un Trabajo Final de Graduación para poder graduarse de Licenciatura. Este equivale a 7 créditos y 21 horas prácticas semanales",3))
        else:
            malla.append(colocar_notasTC("Debe cursarse tres centros de formación humanistica para poder graduarse",1))
            #malla.append(colocar_notasTC("Debe realizarse una Práctica Profesional para poder escoger la salida lateral de bachillerato. Esta equivale a 7 créditos y 315 horas laboradas en un semestre",2))
        cursos_enf = cursos[cursos["area"].isin(lista)]
        for semestre in rango:
            horasteoriasemestre = cursos_enf[cursos_enf.semestre == semestre].horasTeoria.sum()
            horaspracticasemestre = cursos_enf[cursos_enf.semestre == semestre].horasPractica.sum()
            creditossemestre = cursos_enf[cursos_enf.semestre == semestre].creditos.sum()
            malla.append(colocar_semestre(semestre,sesgo,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        for id in cursos_enf.id:
            semestre = cursos_enf[cursos_enf.id == id].semestre.item()
            codigo = cursos_enf[cursos_enf.id == id].codigo.item()
            nombre = cursos_enf[cursos_enf.id == id].nombre.item()
            fila = cursos_enf[cursos_enf.id == id].fila.item()
            horasteoria = cursos_enf[cursos_enf.id == id].horasTeoria.item()
            horaspractica = cursos_enf[cursos_enf.id == id].horasPractica.item()
            creditos = cursos_enf[cursos_enf.id == id].creditos.item()
            aprob = cursos_enf[cursos_enf.id == id][año].item() 
            if aprob == "A":
                color = "green!20!white"
            else:
                color = "white"
            if semestre >= sesgo:
                requi = cursos_enf[cursos_enf.id == id].requisitos.str.split(';',expand=True)
                corequi = str(cursos_enf[cursos_enf.id == id].correquisitos.item())                           
                malla.append(colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color))
                if not(requi[0].isna().item()):
                    for column in requi.columns:
                        idreq = requi[column].item()
                        # print(id)
                        # print(idreq)
                        codreq = cursos_enf[cursos_enf.id == idreq].codigo.item()
                        semreq = cursos_enf[cursos_enf.id == idreq].semestre.item()
                        filareq = cursos_enf[cursos_enf.id == idreq].fila.item()
                        sevesreq = cursos_enf[cursos_enf.id == idreq].sevesreq.item()
                        sevreq = cursos_enf[cursos_enf.id == id].sevreq.item() 
                        if semestre > sesgo:
                            if (filareq == fila) and (semreq == semestre - 1):
                                malla.append(colocar_arrowreq(semestre,sesgo,fila,-0.7,"black"))
                            elif ((filareq == fila - 1) or (filareq == fila + 1)) and (semreq == semestre - 1):
                                if (filareq == fila - 1):
                                    dir = -1
                                if (filareq == fila + 1):
                                    dir = 1
                                malla.append(colocar_arrowreqs(semestre,sesgo,fila,dir,"black"))                   
                            else:
                                reqcounter +=1
                                malla.append(colocar_diareq(semestre,sesgo,fila,sevreq,reqcounter,"black"))
                                malla.append(colocar_diaesreq(semreq,sesgo,filareq,sevesreq + 0.9,reqcounter,"black"))
                                cursos_enf.loc[cursos_enf['id'] == idreq, 'sevesreq'] = sevesreq + 1
                                cursos_enf.loc[cursos_enf['id'] == id, 'sevreq'] = sevreq + 1.8
                if not(corequi == 'nan'):
                    semcoreq = cursos_enf[cursos_enf.id == corequi].semestre.item()
                    filacoreq = cursos_enf[cursos_enf.id == corequi].fila.item()
                    if ((filacoreq == fila - 1) or (filacoreq == fila + 1)) and (semcoreq == semestre):
                        if (filacoreq == fila - 1):
                            dir = -1
                        if (filacoreq == fila + 1):
                            dir = 1
                        malla.append(colocar_arrowcoreq(semestre,sesgo,fila,dir,"black"))
                    else:
                        reqcounter +=1
                        malla.append(colocar_triacoreq(semestre,sesgo,fila,reqcounter,"black"))
                        malla.append(colocar_triaescoreq(semcoreq,sesgo,filacoreq,reqcounter,"black"))

def malla_carnet(malla,cursos,sesgo,lista,titulo,rango,enf):
        reqcounter = 0
        malla.append(colocar_titulo(titulo,"lightgray"))
        if enf:
            malla.append(colocar_recreq("Electivas","Notas","lightgray"))
            malla.append(colocar_notas("Cursos del tronco común en color blanco",1))
            malla.append(colocar_notas("Debe escogerse 2 de las 9 electivas posibles para cursarlas en el décimo semestre",2))
            malla.append(colocar_notas("Debe realizarse un Trabajo Final de Graduación para poder graduarse de Licenciatura. Este equivale a 7 créditos y 21 horas prácticas semanales",3))
        else:
            malla.append(colocar_notasTC("Debe cursarse tres centros de formación humanistica para poder graduarse",1))
            #malla.append(colocar_notasTC("Debe realizarse una Práctica Profesional para poder escoger la salida lateral de bachillerato. Esta equivale a 7 créditos y 315 horas laboradas en un semestre",2))
        cursos_enf = cursos[cursos["area"].isin(lista)]
        for semestre in rango:
            horasteoriasemestre = cursos_enf[cursos_enf.semestre == semestre].horasTeoria.sum()
            horaspracticasemestre = cursos_enf[cursos_enf.semestre == semestre].horasPractica.sum()
            creditossemestre = cursos_enf[cursos_enf.semestre == semestre].creditos.sum()
            malla.append(colocar_semestre(semestre,sesgo,"lightgray",horasteoriasemestre,horaspracticasemestre,creditossemestre))            
        for id in cursos_enf.id:
            semestre = cursos_enf[cursos_enf.id == id].semestre.item()
            codigo = cursos_enf[cursos_enf.id == id].codigo.item()
            nombre = cursos_enf[cursos_enf.id == id].nombre.item()
            fila = cursos_enf[cursos_enf.id == id].fila.item()
            horasteoria = cursos_enf[cursos_enf.id == id].horasTeoria.item()
            horaspractica = cursos_enf[cursos_enf.id == id].horasPractica.item()
            creditos = cursos_enf[cursos_enf.id == id].creditos.item()
            aprob = cursos_enf[cursos_enf.id == id]["aprobadas"].item() 
            if aprob == "A":
                color = "green!20!white"
            else:
                color = "white"
            if semestre >= sesgo:
                requi = cursos_enf[cursos_enf.id == id].requisitos.str.split(';',expand=True)
                corequi = str(cursos_enf[cursos_enf.id == id].correquisitos.item())                           
                malla.append(colocar_curso(codigo,nombre,fila,semestre,sesgo,horasteoria,horaspractica,creditos,color))
                if not(requi[0].isna().item()):
                    for column in requi.columns:
                        idreq = requi[column].item()
                        # print(id)
                        # print(idreq)
                        codreq = cursos_enf[cursos_enf.id == idreq].codigo.item()
                        semreq = cursos_enf[cursos_enf.id == idreq].semestre.item()
                        filareq = cursos_enf[cursos_enf.id == idreq].fila.item()
                        sevesreq = cursos_enf[cursos_enf.id == idreq].sevesreq.item()
                        sevreq = cursos_enf[cursos_enf.id == id].sevreq.item() 
                        if semestre > sesgo:
                            if (filareq == fila) and (semreq == semestre - 1):
                                malla.append(colocar_arrowreq(semestre,sesgo,fila,-0.7,"black"))
                            elif ((filareq == fila - 1) or (filareq == fila + 1)) and (semreq == semestre - 1):
                                if (filareq == fila - 1):
                                    dir = -1
                                if (filareq == fila + 1):
                                    dir = 1
                                malla.append(colocar_arrowreqs(semestre,sesgo,fila,dir,"black"))                   
                            else:
                                reqcounter +=1
                                malla.append(colocar_diareq(semestre,sesgo,fila,sevreq,reqcounter,"black"))
                                malla.append(colocar_diaesreq(semreq,sesgo,filareq,sevesreq + 0.9,reqcounter,"black"))
                                cursos_enf.loc[cursos_enf['id'] == idreq, 'sevesreq'] = sevesreq + 1
                                cursos_enf.loc[cursos_enf['id'] == id, 'sevreq'] = sevreq + 1.8
                if not(corequi == 'nan'):
                    semcoreq = cursos_enf[cursos_enf.id == corequi].semestre.item()
                    filacoreq = cursos_enf[cursos_enf.id == corequi].fila.item()
                    if ((filacoreq == fila - 1) or (filacoreq == fila + 1)) and (semcoreq == semestre):
                        if (filacoreq == fila - 1):
                            dir = -1
                        if (filacoreq == fila + 1):
                            dir = 1
                        malla.append(colocar_arrowcoreq(semestre,sesgo,fila,dir,"black"))
                    else:
                        reqcounter +=1
                        malla.append(colocar_triacoreq(semestre,sesgo,fila,reqcounter,"black"))
                        malla.append(colocar_triaescoreq(semcoreq,sesgo,filacoreq,reqcounter,"black"))

def generar_malla_carnet(cursos,carnet):
    #Geometría
    geometry_options = { 
        "left": "0mm",
        "right": "0mm",
        "top": "1mm",
        "bottom": "0mm",
        "headheight": "1mm",
        "footskip": "1mm"
    }
    #Opciones del documento
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper","landscape"],
                   geometry_options=geometry_options)
    #Paquetes
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish',"activeacute"]))
    doc.packages.append(Package(name="graphicx"))
    doc.packages.append(Package(name="tikz"))
    doc.packages.append(Package(name="anyfontsize"))
    doc.packages.append(Package(name="xcolor",options="dvipsnames"))
    doc.packages.append(Package(name="colortbl"))
    doc.packages.append(Package(name="array"))
    doc.packages.append(Package(name="float"))
    doc.packages.append(Package(name="longtable"))
    doc.packages.append(Package(name="multirow"))
    doc.packages.append(Package(name="fancyhdr"))
    doc.preamble.append(NoEscape(r'\usetikzlibrary{arrows.meta}'))
    #Bloques
    bloqueTitulo = NoEscape(
    r'''\tikzset{
            pics/titulo/.style args={#1,#2}{
            code={
                \def\ancho{57}
                \def\alto{0.7}
                \draw[fill=#2] (-\ancho/2-2,2*\alto) rectangle (\ancho/2+2,-2*\alto) node[midway,align=center,text width=45cm]{\fontsize{30pt}{0pt}\selectfont \textbf{#1}};
            }
        }
    }'''
    )
    bloqueCurso = NoEscape(
    r'''\tikzset{
            pics/curso/.style args={#1,#2,#3,#4,#5,#6}{
            code={
                \def\ancho{5}
                \def\alto{0.8}
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,-\alto) node[midway,align=center,text width=\ancho cm]{\fontsize{16pt}{2pt}\selectfont {#2}};
                \draw[fill=#6] (-\ancho/2,\alto) rectangle (\ancho/2,\alto + \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #1};
                \draw[fill=#6] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #3};
                \draw[fill=#6] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #4};
                \draw[fill=#6] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{14pt}{14pt}\selectfont #5};
            }
        }
    }''' 
    #1: codigo, #2: nombre, #3: horasteoria, #4: horaspractica, #5: creditos, #6: color
    )
    bloqueSemestre = NoEscape(
    r'''\tikzset{
            pics/semestre/.style args={#1,#2,#3,#4,#5}{
            code={
                \def\ancho{6}
                \def\alto{0.8}
                \draw[fill=#2] (-\ancho/2,1.5*\alto) rectangle (\ancho/2,-1.5*\alto) node[midway,align=center,text width=\ancho cm]{\fontsize{16pt}{12pt}\selectfont \textbf{#1}};
                \draw[fill=#2] (-\ancho/2,-\alto) rectangle (-\ancho/2 + \ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #3};
                \draw[fill=#2] (-\ancho/2 + \ancho/3,-\alto) rectangle (-\ancho/2 + 2*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #4};
                \draw[fill=#2] (-\ancho/2 + 2*\ancho/3,-\alto) rectangle (-\ancho/2 + 3*\ancho/3, -\alto - \alto) node[midway]{\fontsize{12pt}{14pt}\selectfont #5};
            }
        }
    }'''
    #1: semestre, #2: color, #3: horasteoria, #4: horaspractica, #5: creditos
    )
    
    doc.preamble.append(bloqueTitulo)        
    doc.preamble.append(bloqueCurso)
    doc.preamble.append(bloqueSemestre)

    doc.append(Command('centering'))
    sesgo = 0
    rango = range(0,9)
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_TRC:
        titulo = "Tronco común de Licenciatura en Ingeniería Electromecánica y salida lateral de Bachillerato en Ingeniería Electromecánica"
        malla_carnet(malla_TRC,cursos,sesgo,TRC,titulo,rango,False)
    doc.append(NoEscape(r"\newpage"))
    sesgo = 7
    rango = range(7,11)
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_INS:
        titulo = "Licenciatura en Ingeniería Electromecánica con énfasis en Instalaciones Electromecánicas"
        malla_carnet(malla_INS,cursos,sesgo,INS,titulo,rango,True)
    doc.append(NoEscape(r"\newpage"))
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_AER:
        titulo = "Licenciatura en Ingeniería Electromecánica con énfasis en Aeronáutica"
        malla_carnet(malla_AER,cursos,sesgo,AER,titulo,rango,True)
    doc.append(NoEscape(r"\newpage"))
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_SCF:
        titulo = "Licenciatura en Ingeniería Electromecánica con énfasis en Sistemas Ciberfísicos"
        malla_carnet(malla_SCF,cursos,sesgo,SCF,titulo,rango,True)
    doc.generate_pdf(f"malla_EM_{carnet}", clean=True, clean_tex=False, compiler='lualatex',silent=True)