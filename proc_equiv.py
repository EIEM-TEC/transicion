import pandas as pd

TRClist = ["ADD","AUT","CIB","CYD","FPH","IEE","IMM"]

mallaEE = pd.read_csv("https://raw.githubusercontent.com/EIEM-TEC/CLIE/refs/heads/main/cursos/cursos_malla.csv")
mallaMI = pd.read_csv("malla_MI.csv")
mallaMInom =pd.read_csv("cursos_MI.csv")
equiv = pd.read_csv("equivalencias.csv")

equiv["codigoMI"] = equiv["codigoMI"].str.split(";",expand=False)
equiv = equiv.explode("codigoMI")
equiv = equiv.merge(mallaEE[["id", "codigo", "creditos", "nombre", "area"]], left_on="codigoEE", right_on="codigo", how="left").drop(columns=["codigo"])
equiv['id'] = equiv['id'].str[3:]
equiv.loc[equiv['area'].isin(TRClist), 'area'] = 'TRC'
equiv['id'] = equiv['area'] + equiv['id']
equiv = equiv.merge(mallaMInom[["codigo", "nombre"]], left_on="codigoMI", right_on="codigo", how="left").drop(columns=["codigo"])
equiv.rename(columns={'codigoEE': 'codIEM', 'codigoMI': 'codEquiIMI', 'direccion': 'bidireccional', 'nombre_x': 'nombreIEM', 'nombre_y': 'nombresIMI'}, inplace=True)
equiv = equiv.fillna('-')
print(equiv)
equiv['codEquiIMI'] = equiv['codEquiIMI'].apply(lambda x: x + f" ({mallaMI[mallaMI["codigo"]==x].creditos.iloc[0]})" if x != '-' and not mallaMI[mallaMI['codigo'] == x].empty else x)
equiv = equiv.groupby('id', as_index=False).agg({
    'area': 'first',
    'codIEM': 'first',
    'nombreIEM': 'first',
    'codEquiIMI': lambda x: ' '.join(x.unique()),
    'nombresIMI': lambda x: ' y '.join(x.unique()),
    'bidireccional': 'first',
})
equiv = equiv.fillna('-')
equiv['codIEM'] = equiv['codIEM'].apply(lambda x: x + f"   ({mallaEE[mallaEE["codigo"]==x].creditos.iloc[0]})" if x != '-' and not mallaEE[mallaEE['codigo'] == x].empty else x)
equiv['bidireccional'] = equiv['bidireccional'].map({1: 'Si', 0: 'No'})
area_order = ['TRC', 'INS', 'AER', 'SCF']
equiv['area'] = pd.Categorical(equiv['area'], categories=area_order, ordered=True)
equiv = equiv.sort_values(by=['area', 'id']).reset_index(drop=True).drop(columns="area")


#equivnom = equivnom[[]]

equiv.to_csv("equivalencias_nombre.csv",index=False)