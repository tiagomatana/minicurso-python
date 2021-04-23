

import pandas as pd # pip install openpyxl
import os

myPath = os.path.abspath(os.getcwd())
Base = "Vendas.xlsx"

tabela_vendas = pd.read_excel(myPath+"/"+Base)

# exibir a base completa sem ocultar linhas e colunas
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# print(tabela_vendas)


# faturamento por loja
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
# print(faturamento)
# quantidade de produtos vendidos por loja
quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
# print(quantidade)
# ticket médio por produto
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
print(ticket_medio)
# enviar email com relatorio


