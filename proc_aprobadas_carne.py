import funciones as fun
import pandas as pd
from pylatex import Document, Package, Command,\
    simple_page_number,\
    TikZ, TikZOptions
from pylatex.utils import NoEscape, bold, italic



mallaEE = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv")
#mallaEE = pd.read_csv("cursos_malla.csv")
mallaMI = pd.read_csv("malla_MI.csv")
equiv = pd.read_csv("equivalencias.csv")
est = pd.read_csv("datos\\2021_2025.csv")

areas = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/areas.csv")

TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]
INS = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS"]
AER = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","AER"]
SCF = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","SCF"]

def generar_malla_carnet(mallaEE,lista):
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
        fun.malla_enf(malla_TRC,mallaEE,sesgo,TRC,titulo,rango,False,año)
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
        fun.malla_enf(malla_INS,mallaEE,sesgo,INS,titulo,rango,True,año)
    doc.append(NoEscape(r"\newpage"))
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_AER:
        titulo = "Licenciatura en Ingeniería Electromecánica con énfasis en Aeronáutica"
        fun.malla_enf(malla_AER,mallaEE,sesgo,AER,titulo,rango,True,año)
    doc.append(NoEscape(r"\newpage"))
    with doc.create(TikZ(
            options=TikZOptions
                (    
                "scale = 0.45",
                "transform shape"
                )
        )) as malla_SCF:
        titulo = "Licenciatura en Ingeniería Electromecánica con énfasis en Sistemas Ciberfísicos"
        fun.malla_enf(malla_SCF,cursos,sesgo,SCF,titulo,rango,True,año)
    doc.generate_pdf(f"malla_EM_{año}", clean=True, clean_tex=False, compiler='lualatex',silent=True)

def por_carnet(carnet,estudiantes):
    lista ,nombre= fun.aprobadas_carne(carnet,estudiantes)
    creditosIMI,\
    creditosTRC,\
    creditosINS,\
    creditosAER,\
    creditosSCF,\
    equivfinal=\
    fun.obtener_equiv_lista(
        mallaEE,
        mallaMI,
        equiv,
        lista,
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
    print(f"\nPara {nombre}:")
    print(f"Créditos en IMI: {creditosIMI}, porcentaje: {porcIMI*100} %")
    print(f"Créditos en TRC: {creditosTRC}, porcentaje: {porcTRC*100} %")
    print(f"Créditos en INS: {creditosINS}, porcentaje: {porcINS*100} %")
    print(f"Créditos en AER: {creditosAER}, porcentaje: {porcAER*100} %")
    print(f"Créditos en SCF: {creditosSCF}, porcentaje: {porcSCF*100} %\n")
    return equivfinal



carnetmare = 2021023053
carnetangi = 2023234861


por_carnet(carnetmare,est)

por_carnet(carnetangi,est)
