
from flask import request, jsonify
from app import app, auth
from app.scrapping.crawler import get_title, get_content
from app.data.producao import get_content_producao
from app.data.processamento import get_content_processamento
from app.data.comercializacao import get_content_comercializacao
 
#PRODUCAO
@app.route('/scrape/vitiproducao', methods=['GET'])
@auth.login_required
def scrape_viti_producao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    year = request.args.get('year')
    url = url.split("?")[0] + "?ano=" + year + "&" + url.split("?")[1]
     
    #if not url:
    #   return jsonify({"error": "URL é obrigatória"}), 400
    return get_content_producao(url,year)

#PROCESSAMENTO
@app.route('/scrape/vitiprocessamento', methods=['GET'])
@auth.login_required
def scrape_viti_processamento():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"
    year = request.args.get('year')
    url = url.split("?")[0] + "?ano=" + year + "&" + url.split("?")[1]
    
    return get_content_processamento(url,year)

#COMERCIALIZAÇÃO
@app.route('/scrape/viticomercializacao', methods=['GET'])
@auth.login_required
def scrape_viti_comercializacao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04"
    year = request.args.get('year')
    url = url.split("?")[0] + "?ano=" + year + "&" + url.split("?")[1]
    
    return get_content_comercializacao(url,year)
  
@app.route('/scrape/title', methods=['GET'])
@auth.login_required
def scrape_title():
    """
    Extrai o título de uma página web fornecida pela URL.
    ---
    security:
      - BasicAuth: []
    parameters:
      - name: url
        in: query
        type: string
        required: true
        description: URL da página web para extrair o título.
    responses:
      200:
        description: Título da página web.
        schema:
          type: object
          properties:
            title:
              type: string
              description: O título da página.
      400:
        description: Erro de requisição.
      401:
        description: Não autorizado.
    """
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL é obrigatória"}), 400
    return get_title(url)

@app.route('/scrape/content', methods=['GET'])
@auth.login_required
def scrape_content():
    """
    Extrai cabeçalhos e parágrafos de uma página web fornecida pela URL.
    ---
    security:
      - BasicAuth: []
    parameters:
      - name: url
        in: query
        type: string
        required: true
        description: URL da página web para extrair o conteúdo.
    responses:
      200:
        description: Conteúdo da página web.
        schema:
          type: object
          properties:
            headers:
              type: array
              items:
                type: string
              description: Lista de cabeçalhos (h1, h2, h3).
            paragraphs:
              type: array
              items:
                type: string
              description: Lista de parágrafos.
      400:
        description: Erro de requisição.
      401:
        description: Não autorizado.
    """
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL é obrigatória"}), 400
    return get_content(url)