import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag
from flask import jsonify
import requests

def get_content_exportacao(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        #  Looking for data range (1970 to 2023)
        label = soup.find('label', class_='lbl_pesq')
        rangeAno = label.text.replace("[", "").replace("Ano:", "").replace("]", "").strip()
        rangeAno = rangeAno.split('-')

        consulta = {"Exportacao": []}

        for ano in range(int(rangeAno[0]), int(rangeAno[1]) + 1):
            
            for subconsulta in (range(1, 5)) :
                if subconsulta == 1: 
                    subconsulta_desc = "Vinhos de Mesa"
                elif subconsulta == 2: 
                    subconsulta_desc = "Espumantes"
                elif subconsulta == 3: 
                    subconsulta_desc = "Uvas Frescas"
                elif subconsulta == 4: 
                    subconsulta_desc = "Suco de Uva"
                
                #Composing the URL based on the sub options available in the page 
                urlAno = url.split("?")[0] + "?ano=" + str(ano) + "&" + url.split("?")[1] + "&subopcao=subopt_0" + str(subconsulta)
                response = requests.get(urlAno)
                soup = BeautifulSoup(response.text, 'html.parser')

                #  Looking for the table with the classes 'tb_base tb_dados'
                table = soup.find('table', class_='tb_base tb_dados')
                if not table:
                    continue  # skipping in case of table is not found

                # Initializing variables 
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
                                "unidade_medida": unidadeMedida,
                                "tipo" : subconsulta_desc
                            })

        if response == 200:
            df = pd.DataFrame(consulta['Exportacao'])

            with pd.ExcelWriter('.\\results_exportacao.xlsx') as writer:
                df.to_excel(writer, sheet_name='exportacao', index=False)
 
        return jsonify(consulta)

    except Exception as e:
        return jsonify({"Error - Exportacao":str(e)}),500