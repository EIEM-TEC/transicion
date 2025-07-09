import pandas as pd
from pylatex import Document, Package, Section, Command, Tabularx, PageStyle, Head, Foot, NewPage,\
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

    with doc.create(Section('Información del estudiante', numbering=False)):
        with doc.create(Tabularx(table_spec=r"p{4cm}p{10cm}")) as table:
            table.add_row(["Carnet:",str(carnet)])
            table.add_row(["Nombre:",nombre])
        doc.append(NewLine())
        with doc.create(Tabularx(table_spec=r"p{10cm}p{4cm}")) as table:
            table.add_row(["Créditos aprobados en Mantenimiento Industrial:", str(creditosIMI)])
            table.add_row(["Créditos reconocidos en el tronco común:", str(creditosTRC)])
            table.add_row(["Créditos reconocidos en INS:", str(creditosINS)])
            table.add_row(["Créditos reconocidos en AER:", str(creditosAER)])
            table.add_row(["Créditos reconocidos en SCF:", str(creditosSCF)])
        doc.append(NewLine())
        doc.append(NewLine())
        doc.append('Nota: Este reporte se genera a partir de la información de los cursos aprobados por el estudiante, y puede no reflejar el estado actual del estudiante en el sistema académico.')

    # Add a subsection
    with doc.create(Section('Materias reconocidas', numbering=False)):
        for _,row in equiv.iterrows():
            with doc.create(Tabularx(table_spec=r"p{1.5cm}p{10cm}")) as table:
                table.add_row([bold(row.codigoEE),f"{row.nombre} ({row.creditos})"])
                table.add_row(["",bold("Reconocido por: ")])
            doc.append(NewLine())
            with doc.create(Tabularx(table_spec=r"p{1.5cm}p{1.5cm}p{10cm}")) as table:
                codigosMI = row.codigoMI.split(';')
                for codigo in codigosMI:
                    table.add_row(["",codigo,f"{cursosMI[cursosMI['codigo']==codigo]['nombre'].item()} ({mallaMI[mallaMI['codigo']==codigo]['creditos'].item()})"])
            doc.append(NewLine())
            doc.append(NewLine())
        doc.append(NewLine())
        doc.append('Nota: Cantidad de créditos mostrada entre paréntesis.')

    doc.generate_pdf(f"reportes\\{nombre}", clean=True, clean_tex=True, compiler='lualatex',silent=True)


carnet = 2022055783 # kendall
    
generar_reporte(carnet, estudiantes, cursos, mallaMI, equiv)
