import requests
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag
from flask import jsonify

def get_content_importacao(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        #  Looking for data range (1970 to 2023)
        label = soup.find('label', class_='lbl_pesq')
        rangeAno = label.text.replace("[", "").replace("Ano:", "").replace("]", "").strip()
        rangeAno = rangeAno.split('-')
        consulta = {"Importacao": []}

        for ano in range(int(rangeAno[0]), int(rangeAno[1]) + 1):
            for subconsulta in (range(1, 6)) :
                if subconsulta == 1: 
                    subconsulta_desc = "Vinhos de Mesa"
                elif subconsulta == 2: 
                    subconsulta_desc = "Espumantes"
                elif subconsulta == 3: 
                    subconsulta_desc = "Uvas Frescas"
                elif subconsulta == 4: 
                    subconsulta_desc = "Uvas de Passas"
                elif subconsulta == 5: 
                    subconsulta_desc = "Suco de Uvas"
                
                #Composing the URL based on the sub options available in the page               
                urlAno = url.split("?")[0] + "?ano=" + str(ano) + "&" + url.split("?")[1]+ "&subopcao=subopt_0" + str(subconsulta)

                response = requests.get(urlAno)
                soup = BeautifulSoup(response.text, 'html.parser')
                urlAno = ""
                
                #Looking for the table with the classes 'tb_base tb_dados'
                table = soup.find('table', class_='tb_base tb_dados')


                #Initialize vars
                unidadeMedida = "Kilo"
                
                # Collecting Ddata
                for row in table.tbody.find_all('tr'):
                    columns = row.find_all('td')
                    if columns:
                        paises = columns[0].text.rstrip('\n').strip()
                        quantidade = columns[1].text.rstrip('\n').strip()
                        valor = columns[2].text.rstrip('\n').strip()

                        if paises:
                            consulta["Importacao"].append(
                            {
                                "ano": ano,
                                "paises": paises,
                                "quantidade": quantidade,
                                "valor": valor,
                                "medida": unidadeMedida, 
                                "tipo" : subconsulta_desc
                            })
        if response == 200:
            df = pd.DataFrame(consulta['Importacao'])

            with pd.ExcelWriter('.\\results_importacao.xlsx') as writer:
                df.to_excel(writer, sheet_name='importacao', index=False)

        return jsonify(consulta)

    except Exception as e:
        return jsonify({"Error - Importacao": str(e)}), 500