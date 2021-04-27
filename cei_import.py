class ImportCei:
    
    """Script to generate the stocks' descriptions to use in "Declaração de Imposto de Renda Pessoa Física (DIRPF)" through CEI's reports.
    Help to fill the "Fica de Bens e Direitos.
    
    This class receive one specific file, that have some user informations about your stocks wallet.
    The raw file pass for some slices, rows transformations, joins to clean it.
    One step (function) we use a webscrapping method to rename some rows for a single pattern.
    Once a time whether file are cleanned and reclassified, the class can develop a new arquive to apply the objective.
    
    Attributes:
        archive: a path about the raw file to transform (specific file, downloaded at https://cei.b3.com.br/CEI_Responsivo/extrato-bmfbovespa.aspx)
    """

    def __init__(self, archive):
        """directory "str" from archive(xsl)"""
        self.__archive = archive

    def import_archive(self):
        """import archive:
        usecols=('B:K') and "header=10" will be the same everytime ?
        exclude rows with all values == NaN
        exclude columns with all values == NaN
        converting the index (axis=column) to date"""


        from pandas import read_excel, DataFrame

        try:
            self.__archive_cei_records = read_excel(self.__archive, index_col=5, header=19)
            self.__archive_cei_records = self.__archive_cei_records.loc[:'VALORIZAÇÃO EM REAIS'].drop(['VALORIZAÇÃO EM REAIS'])
            self.__archive_cei_records = self.__archive_cei_records.drop(columns='Cód. Neg.')
            self.__archive_cei_records.dropna(axis='columns', how='any', inplace=True)
            self.__archive_cei_records.columns = ['Empresa', 'Ticker', 'Quantidade', 'Preço', 'ValorTotal']
            self.__archive_cei_records.reset_index(inplace=True)
            self.__archive_cei_records['Empresa'] = self.__archive_cei_records['Ativo']\
                                                    + self.__archive_cei_records['Empresa']
            self.__archive_cei_records = self.__archive_cei_records.drop(columns='Ativo')
            self.__archive_cei_records['Category'] = self.__insert_type_column(column_index=0)
            self.__archive_cei_records['Data'] = self.__search_date()
            self.__archive_cei_records['ORIGEM'] = 'CUSTÓDIA'
            self.__check_sub_ticker()
        except:
            self.__archive_cei_records = DataFrame(data={"NÃO FORAM ENCONTRADOS ATIVOS SOB CUSTÓDIA":[0]})

    def __search_date(self):
        """Import the archive raw and only find the file's month"""

        from pandas import read_excel
        from datetime import datetime

        months_pt_us = {'Janeiro': 'January',
                        'Fevereiro': 'February',
                        'Março': 'March',
                        'Abril': 'April',
                        'Maio': 'May',
                        'Junho': 'June',
                        'Julho': 'July',
                        'Agosto': 'August',
                        'Setembro': 'September',
                        'Outubro': 'October',
                        'Novembro': 'November',
                        'Dezembro': 'December'}

        date = read_excel(self.__archive,
                                         header=6)
        date = date.columns[0]
        date = " ".join(months_pt_us.get(i, i) for i in date.split())
        date = datetime.strptime(date, '%B de %Y')
        date = str(date.strftime('%m-%Y'))
        return date

    def __check_type(self, value):
        """look for a pattern and categorize in a type (acao, etf ou fii)"""
        import re
        patternci = "[C]{1}[I]{1}"
        validateci = re.search(patternci, value)

        try:
            validateci.group() == 'CI'
            if value.startswith('FII') and validateci.group() == 'CI':
                return 'FII'
            else:
                value.endswith('CI')
                return 'ETF'
        except:
            if value.startswith('FII'):
                return 'FII'
            else:
                return 'ACAO'

    def __insert_type_column(self, column_index):
        """loop to include one column with the category in df_formated"""
        """column_index == 'Empresa' """
        column_type = []
        for i in range(0, len(self.__archive_cei_records)):
            row = self.__archive_cei_records.iloc[i, column_index]
            type_found = self.__check_type(row)
            column_type.append(type_found)
        return column_type

    def __check_sub_ticker(self):
        """after check_type for each assets pattern and insert the type,
            use index to drop some tickers that means anothers unusual custody,
            like 'direito de subscrição'"""
        index_drop = []

        for i in range(0, (len(self.__archive_cei_records) - 1)):
            if self.__archive_cei_records.iloc[i][5] == 'ACAO':
                end_acao = [1, 2, 9, 10]
                ticker = self.__archive_cei_records.iloc[i][1]
                if int(ticker[4:]) in end_acao:
                    index_drop.append(self.__archive_cei_records.iloc[i].name)
                else:
                    pass
            elif self.__archive_cei_records.iloc[i][5] == 'FII':
                end_fii = [12, 13, 14, 15]
                ticker = self.__archive_cei_records.iloc[i][1]
                if int(ticker[4:]) in end_fii:
                    index_drop.append(self.__archive_cei_records.iloc[i].name)
                else:
                    pass
            else:
                pass

        self.__archive_cei_records.drop(index_drop, inplace=True)

#class TableFormatted(ImportCei):
    def df_records(self):
        """show a df from archive formated (custody assets), after import and cleanned"""
        return self.__archive_cei_records

    def dfs_records_csv(self):
        """return a .csv from archive formated (custody assets), after import and cleanned"""
        df = self.__archive_cei_records
        file_title = 'relatorio_' + self.__search_date() + '.xlsx'
        return df.to_excel(file_title, encoding='latin-1', index=False, sheet_name='CUSTODIA')

#class Irpf(ImportCei):
    def __irpf_description(self):
        """develop a .csv from archive formated (irpf_description), after import and cleanned.
            Into a loop using asset category, make a web scrapping to return the required infos.
            Use the required infos to concat a irpf description pattern."""

        from bs4 import BeautifulSoup
        import requests
        from pandas import DataFrame

        historicos = []
        cnpj_web = []
        saldo = []
        category = []
        codigo = []

        for i in range(0, len(self.__archive_cei_records)):
            if self.__archive_cei_records.iloc[i][5] == 'ACAO':
                ticker = self.__archive_cei_records.iloc[i][1].strip()
                quantidade = int(self.__archive_cei_records.iloc[i][2])
                saldo_ticker = str(self.__archive_cei_records.iloc[i][4])
                saldo_ticker = saldo_ticker.replace(".", ",")
                url = f'https://statusinvest.com.br/acoes/{ticker.lower()}'
                html = requests.get(url).content
                soup = BeautifulSoup(html, 'html.parser')
                cnpj = soup.find('small', class_="d-block fs-4 fw-100 lh-4")
                name = soup.find('span', class_="d-block fw-600 text-main-green-dark")
                h_acoes = f'{quantidade} COTAS AÇÕES - {name.string} - {ticker}'
                cnpj_web.append(cnpj.string)
                historicos.append(h_acoes)
                saldo.append(saldo_ticker)
                category.append(self.__archive_cei_records.iloc[i][5])
                codigo.append(31)
            elif self.__archive_cei_records.iloc[i][5] == 'FII':
                ticker = self.__archive_cei_records.iloc[i][1].strip()
                quantidade = int(self.__archive_cei_records.iloc[i][2])
                saldo_ticker = str(self.__archive_cei_records.iloc[i][4])
                saldo_ticker = saldo_ticker.replace(".", ",")
                url = f'https://www.fundsexplorer.com.br/funds/{ticker.lower()}'
                html = requests.get(url).content
                soup = BeautifulSoup(html, 'html.parser')
                name = soup.find('h3', class_="section-subtitle")
                cnpj = soup.find(id="basic-infos")
                cnpj = cnpj.find_all(class_="col-md-6 col-xs-12")[1]
                cnpj = cnpj.find('span', class_="description")
                h_fii = f'{quantidade} COTAS FUNDO IMOBILIÁRIO - {name.string} - {ticker}'
                cnpj_web.append(cnpj.string.strip())
                historicos.append(h_fii)
                saldo.append(saldo_ticker)
                category.append(self.__archive_cei_records.iloc[i][5])
                codigo.append(73)
            else:
                ticker = self.__archive_cei_records.iloc[i][1].strip()
                quantidade = int(self.__archive_cei_records.iloc[i][2])
                saldo_ticker = str(self.__archive_cei_records.iloc[i][4])
                saldo_ticker = saldo_ticker.replace(".", ",")
                url = f'https://statusinvest.com.br/etfs/{ticker.lower()}'
                html = requests.get(url).content
                soup = BeautifulSoup(html, 'html.parser')
                name_cnpj = soup.find(id="company-section")
                name_cnpj = name_cnpj.find('div', class_="top-info info-3 sm d-flex justify-between")
                cnpj = name_cnpj.find_all(class_="info")[7]
                cnpj = cnpj.find('strong', class_="value")
                name = name_cnpj.find_all(class_="info")[8]
                name = name.find('strong', class_="value")
                h_fii = f'{quantidade} COTAS FUNDO FUNDO DE ÍNDICE (ETF) - {name.string} - {ticker}'
                cnpj_web.append(cnpj.string)
                historicos.append(h_fii)
                saldo.append(saldo_ticker)
                category.append(self.__archive_cei_records.iloc[i][5])
                codigo.append(74)

        df = DataFrame({"CATEGORIA": category,
                            "CÓDIGO": codigo,
                            "CNPJ": cnpj_web,
                            "DESCRIMINAÇÃO": historicos,
                            "SALDO": saldo}).sort_values(by=['CÓDIGO']).reset_index(drop=True)

        return df

    def irpf_description_csv(self):
        """Return a .csv from archive formated (irpf_description), after import and cleanned."""
        df = self.__irpf_description()
        file_title = 'historico_irpf_' + self.__search_date() + '.csv'
        return df.to_csv(file_title, encoding='latin-1', index=False)
