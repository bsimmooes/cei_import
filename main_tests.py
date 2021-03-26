"""IMPORTANDO BIBLIOTECA"""
from cei_import import ImportCei
#from cei_import import ImportCei, Irpf, TableFormatted

"""INSTANCIANDO ARQUIVO"""
relatorio = ImportCei('C:/Users/bsimm/PycharmProjects/cei_import/InfoCEI_arquivo_exemplo4.xls')

"""DATA CLEANING NO ARQUIVO INSTANCIADO"""
relatorio.import_archive()

"""GERANDO .CSV DOS ATIVOS EM CUSTÓDIA NO RESPECTIVO MÊS/ANO"""
relatorio.dfs_records_csv()

"""APENAS VISUALIZANDO O DATAFRAME DOS ATIVOS EM CUSTÓDIA NO RESPECTIVO MÊS/ANO"""
print(relatorio.df_records())

"""GERANDO .CSV COM OS HISTÓRICOS/DESCRIÇÕES PARA DIRPF DOS ATIVOS EM CUSTÓDIA NO RESPECTIVO MÊS/ANO"""
relatorio.irpf_description_csv()