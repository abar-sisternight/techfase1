
from flask import request, jsonify
from app import app, auth, config
from app.data.producao import get_content_producao
from app.data.processamento import get_content_processamento
from app.data.comercializacao import get_content_comercializacao
from app.data.importacao import get_content_importacao
from app.data.exportacao import get_content_exportacao
from app.utils.linksviti import url_viti_exportacao, url_viti_importacao, url_viti_processamento, url_viti_producao, url_viti_comercial

#ROUTE PRODUCAO
@app.route('/scrape/vitiproducao', methods=['GET'])
@auth.login_required
def scrape_viti_producao():
    return get_content_producao(url_viti_producao)

#ROUTE PROCESSAMENTO
@app.route('/scrape/vitiprocessamento', methods=['GET'])
@auth.login_required
def scrape_viti_processamento():
    return get_content_processamento(url_viti_processamento)

#ROUTE COMERCIALIZAÇÃO
@app.route('/scrape/viticomercializacao', methods=['GET'])
@auth.login_required
def scrape_viti_comercializacao():
    return get_content_comercializacao(url_viti_comercial)

#ROUTE IMPORTACAO
@app.route('/scrape/vitiimportacao', methods=['GET'])
@auth.login_required
def scrape_viti_importacao():
    return get_content_importacao(url_viti_importacao)

#ROUTE EXPORTACAO
@app.route('/scrape/vitiexportacao', methods=['GET'])
@auth.login_required
def scrape_viti_exportacao():
    return get_content_exportacao(url_viti_exportacao)



 