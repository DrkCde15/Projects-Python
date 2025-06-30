import pandas as pd

#carregando dataset usando o ';' como separador
df_frame = pd.read_csv('./datasets/GasPricesinBrazil_2004-2019_new.csv', sep=';', encoding='latin1')
print(df_frame)

#selecionando 5 primeiras linhas
print(df_frame.head(11))

df_rename = df_frame.rename(columns={'COLUNM': 'COLUNA FINAL'}) #alterando o nome da coluna

# Imprimindo o DataFrame com os novos nomes das colunas
<<<<<<< HEAD
print(df_rename)
=======
print(df_rename)
>>>>>>> a89fd2af1ecce4acfc5d54e25bc5fa56c3c5cb87
