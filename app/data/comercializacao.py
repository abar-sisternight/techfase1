import requests
import pandas as pd
from bs4 import BeautifulSoup, NavigableString, Tag
from flask import jsonify

def get_content_comercializacao(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        #  Looking for data range (1970 to 2023)
        label = soup.find('label', class_='lbl_pesq')
        rangeAno = label.text.replace("[","").replace("Ano:", "").replace("]", "").strip()
        rangeAno = rangeAno.split('-')
        consulta = {"Comercializacao": []}

        for ano in range(int(rangeAno[0]), int(rangeAno[1]) + 1) :
            
            urlAno = url.split("?")[0] + "?ano=" + str(ano) + "&" + url.split("?")[1]
            response = requests.get(urlAno)
            soup = BeautifulSoup(response.text, 'html.parser')
            urlAno = ""
                
            #  Looking for the table with the classes 'wikitable' and 'sortable'
            table = soup.find('table', class_='tb_base tb_dados')
               
            #Initialize vars 
            #nullable data can be found from datasource
            unidadeMedida = "Litro"
            categoria = ""
            item = ""
            quantidade = ""
            
            # Collecting Ddata
            for row in table.tbody.find_all('tr'):    
            
                # Find all columns para categoria for each column
                columns = row.find_all('td', {"class":"tb_item"})
                if(columns != []):
                    categoria = columns[0].text.rstrip('\n').replace("""""","").strip()
    
                else:
                    columnsubItem = row.find_all('td', {"class":"tb_subitem"})
                    
                    if(columnsubItem != []):
                        item = columnsubItem[0].text.strip()
                        quantidade = columnsubItem[1].text.strip()
                
                if len(item) > 0:   
                    #df = df.append({'ano': ano,  'categoria': categoria, 'item': item, 'quantidade': quantidade}, ignore_index=True)  
                    consulta["Comercializacao"].append(
                                    {
                                        "ano" : ano,
                                        "categoria": categoria,
                                        "item": item,
                                        "quantidade": quantidade,
                                        "medida" : unidadeMedida                                                                        
                                    })          
                    item = ""
                    quantidade = ""
        if response == 200:
            df = pd.DataFrame(consulta['Comercializacao'])

            with pd.ExcelWriter('.\\results_comercializacao.xlsx') as writer:
                df.to_excel(writer, sheet_name='comercializacao', index=False)
                
        return jsonify(consulta)
                                    
    except Exception as e:
        return jsonify({"Error - Comercializacao": str(e)}), 500