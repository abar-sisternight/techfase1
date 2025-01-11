import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag
from flask import jsonify
import requests

def get_content_exportacao(url, year):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        consulta = {"Exportacao": []}

        table = soup.find('table', class_='tb_base tb_dados')
        # print(table)

        df = pd.DataFrame(columns=['ano', 'paises', 'quantidade', 'valor'])

        #Initialize vars
        unidadeMedida = "Kilo"
        ano = year
        # categoria = ""
        paises = ""
        quantidade = ""
        valor = ""

        for row in table.tbody.find_all('tr'):    
            # Find all columns para categoria for each column
            columns = row.find_all('td')
            # print(columns)
            if(columns != []):
                paises = columns[0].text.rstrip('\n').replace("""""","").strip()
                quantidade = columns[1].text.rstrip('\n').replace("""""","").strip()
                valor = columns[2].text.rstrip('\n').replace("""""","").strip()
                # print()
            
            if len(paises) > 0:   
                #df = df.append({'ano': ano,  'categoria': categoria, 'item': item, 'quantidade': quantidade}, ignore_index=True)  
                consulta["Exportacao"].append({
                                            "ano" : ano,
                                            # "categoria": categoria,
                                            "paises": paises,
                                            "quantidade": quantidade,
                                            "valor" : valor,
                                            "unicade_medida" : unidadeMedida                                                                   
                                        })          
                # paises = ""
        return jsonify(consulta)
    
    except Exception as e:
        return jsonify({"Error - Exportacao": str(e)}), 500

def get_content_exportacao_full(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Obtendo o intervalo de anos (por exemplo, 1970 a 2023)
        label = soup.find('label', class_='lbl_pesq')
        rangeAno = label.text.replace("[", "").replace("Ano:", "").replace("]", "").strip()
        rangeAno = rangeAno.split('-')

        consulta = {"Exportacao": []}

        # Iterando por cada ano no intervalo
        for ano in range(int(rangeAno[0]), int(rangeAno[1]) + 1):
            urlAno = url.split("?")[0] + "?ano=" + str(ano) + "&" + url.split("?")[1]
            response = requests.get(urlAno)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Buscando a tabela
            table = soup.find('table', class_='tb_base tb_dados')
            if not table:
                continue  # Pular caso não encontre tabela para o ano

            # Inicializando variáveis
            unidadeMedida = "Kilo"

            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    paises = columns[0].text.rstrip('\n').strip()
                    quantidade = columns[1].text.rstrip('\n').strip()
                    valor = columns[2].text.rstrip('\n').strip()

                    if paises:
                        consulta["Exportacao"].append({
                            "ano": ano,
                            "paises": paises,
                            "quantidade": quantidade,
                            "valor": valor,
                            "unicade_medida": unidadeMedida
                        })

        return jsonify(consulta)

    except Exception as e:
        return jsonify({"Error - Exportacao": str(e)}), 500