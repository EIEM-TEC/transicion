import pandas as pd
from pylatex import Document, Package, Section, Subsection, Command, Tabularx, LongTabularx, PageStyle, Head, Foot, NewPage,\
    TextColor, MiniPage, StandAloneGraphic, simple_page_number,\
    TikZ, TikZScope, TikZNode, TikZOptions, TikZCoordinate, TikZNodeAnchor, TikZPath,\
    UnsafeCommand,\
    VerticalSpace, HorizontalSpace, NewLine,\
    LongTable
from pylatex.base_classes import Environment, Arguments
from pylatex.utils import NoEscape, bold, italic
import funciones as fun

cursos = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv")
mallaMI = pd.read_csv("malla_MI.csv")
cursosMI = pd.read_csv("cursos_MI.csv")
cursos['sevesreq'] = cursos['creditos'] * 0.0
cursos['sevreq'] = cursos['creditos'] * 0.0
equiv = pd.read_csv("equivalencias.csv")
estudiantes = pd.read_csv("datos\\2021_2025.csv")

areas = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/areas.csv")
estudiantes = pd.read_csv("datos\\2021_2025.csv")

TRC = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD"]
INS = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","INS"]
AER = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","AER"]
SCF = ["CIB","FPH","CYD","IEE","IMM","AUT","ADD","SCF"]

# black, blue, brown, cyan, darkgray, gray, green, lightgray, lime, magenta, olive, orange, pink, purple, red, teal, violet, white, yellow.

area_colors = {
    "ADD": "blue!20!white",
    "AER": "brown!20!white",
    "AUT": "cyan!20!white",
    "CIB": "green!20!white",
    "CYD": "magenta!20!white",
    "FPH": "olive!20!white",
    "IEE": "orange!20!white",
    "IMM": "red!20!white",
    "INS": "teal!20!white",
    "SCF": "violet!20!white"
}


def generar_reporte(carnet,estudiantes,cursos,mallaMI,equiv):
    #Geometría

    lista ,nombre= fun.aprobadas_carne(carnet,estudiantes)

    creditosIMI,\
    creditosTRC,\
    creditosINS,\
    creditosAER,\
    creditosSCF,\
    equiv=\
    fun.obtener_equiv_lista(
        cursos,
        mallaMI,
        equiv,
        lista,
    )

    print(mallaMI)

    geometry_options = { 
        "left":         "18mm",
        "right":        "18mm",
        "top":          "21mm",
        "bottom":       "21mm",
        "headheight":   "15mm",
        "footskip":     "10mm"
    }

    #Opciones del documento
    doc = Document(documentclass="article", \
                   fontenc=None, \
                   inputenc=None, \
                   lmodern=False, \
                   textcomp=False, \
                   page_numbers=True, \
                   indent=False, \
                   document_options=["letterpaper"],
                   geometry_options=geometry_options)
    #Paquetes
    doc.packages.append(Package(name="fontspec", options=None))
    doc.packages.append(Package(name="babel", options=['spanish',"activeacute"]))
    # doc.packages.append(Package(name="graphicx"))
    # doc.packages.append(Package(name="tikz"))
    # doc.packages.append(Package(name="anyfontsize"))
    # doc.packages.append(Package(name="xcolor",options="dvipsnames"))
    # doc.packages.append(Package(name="colortbl"))
    # doc.packages.append(Package(name="array"))
    # doc.packages.append(Package(name="float"))
    # doc.packages.append(Package(name="longtable"))
    # doc.packages.append(Package(name="multirow"))
    # doc.packages.append(Package(name="fancyhdr"))
    # doc.preamble.append(NoEscape(r'\usetikzlibrary{arrows.meta}'))  
    # Set LongTabularx to have no space between tables and to be left aligned
    doc.preamble.append(NoEscape(r'\setlength{\LTpre}{0pt}'))
    doc.preamble.append(NoEscape(r'\setlength{\LTpost}{0pt}'))
    doc.preamble.append(NoEscape(r'\setlength\LTleft{0pt}'))
    doc.preamble.append(NoEscape(r'\setlength\LTright{0pt}'))

    with doc.create(Subsection('Información del estudiante', numbering=False)):
        doc.append(bold("Carnet: "))
        doc.append(str(carnet))
        doc.append(NewLine())
        doc.append(bold("Nombre: "))
        doc.append(nombre)
        doc.append(NewLine())
        doc.append(bold("Créditos aprobados: "))
        doc.append(str(creditosIMI))

    with doc.create(Subsection('Créditos reconocidos', numbering=False)):
        doc.append(bold("Tronco común y bachillerato: "))
        doc.append(str(creditosTRC))
        doc.append(NewLine())
        doc.append(bold("Énfasis Instalaciones Electromecánicas: "))
        doc.append(str(creditosINS))
        doc.append(NewLine())
        doc.append(bold("Énfasis Aeronaútica: "))
        doc.append(str(creditosAER))
        doc.append(NewLine())
        doc.append(bold("Énfasis Sistemas Ciberfísicos: "))
        doc.append(str(creditosSCF))
    with doc.create(Subsection('Materias reconocidas', numbering=False)):
        doc.append(VerticalSpace("0.5cm"))
        for _,row in equiv.iterrows():
            with doc.create(Tabularx(table_spec=r"p{1.5cm}p{10cm}")) as table:
                table.add_row([bold(row.codigoEE),f"{row.nombre} ({row.creditos})"])
                table.add_row(["",bold("Reconocido por: ")])
            with doc.create(Tabularx(table_spec=r"p{1.5cm}p{1.5cm}p{10cm}")) as table:
                codigosMI = row.codigoMI.split(';')
                for codigo in codigosMI:
                    table.add_row(["",codigo,f"{cursosMI[cursosMI['codigo']==codigo]['nombre'].item()} ({mallaMI[mallaMI['codigo']==codigo]['creditos'].item()})"])
        doc.append('Nota: Cantidad de créditos mostrada entre paréntesis.')

    with doc.create(Section('Materias pendientes', numbering=False)):
        with doc.create(Subsection('Tronco común y bachillerato', numbering=False)):
            with doc.create(LongTabularx(table_spec=r"p{1.5cm}p{10cm}")) as table:
                for _,row in cursos[cursos['area'].isin(TRC)].iterrows():
                    if row.codigo not in lista:
                        table.add_row([bold(row.codigo),f"{row.nombre} ({row.creditos})"])
        with doc.create(Subsection('Énfasis Instalaciones Electromecánicas', numbering=False)):
            with doc.create(LongTabularx(table_spec=r"p{1.5cm}p{10cm}")) as table:
                for _,row in cursos[cursos['area'].isin(INS)].iterrows():
                    if row.codigo not in lista:
                        table.add_row([bold(row.codigo),f"{row.nombre} ({row.creditos})"])
                        

    doc.generate_pdf(f"reportes\\{nombre}", clean=True, clean_tex=False, compiler='lualatex',silent=True)



carnet = 2022055783 # kendall
    
generar_reporte(carnet, estudiantes, cursos, mallaMI, equiv)
