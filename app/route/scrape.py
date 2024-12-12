
from flask import request, jsonify
from app import app, auth
from app.scrapping.crawler import get_title, get_content
from app.data.producao import get_content_producao, get_content_producao_full
from app.data.processamento import get_content_processamento, get_content_processamento_full
from app.data.comercializacao import get_content_comercializacao, get_content_comercializacao_full
 
#PRODUCAO
@app.route('/scrape/vitiproducao', methods=['GET'])
@auth.login_required
def scrape_viti_producao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    #year = request.args.get('year')
    #url = url.split("?")[0] + "?ano=" + year + "&" + url.split("?")[1]
     
    return get_content_producao_full(url)

#PROCESSAMENTO
@app.route('/scrape/vitiprocessamento', methods=['GET'])
@auth.login_required
def scrape_viti_processamento():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"
   
    return get_content_processamento_full(url)

#COMERCIALIZAÇÃO
@app.route('/scrape/viticomercializacao', methods=['GET'])
@auth.login_required
def scrape_viti_comercializacao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04"
    
    return get_content_comercializacao_full(url)
 