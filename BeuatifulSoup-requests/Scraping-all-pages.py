'''
OBJETIVO: Dando evolução ao objetivo do programa anterior, a intenção agora é utilizar
as mesmas ferramentas para navegas por todas as páginas e extrair os mesmos dados.
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd


def pageScraper(url, data_dicts):
    # essa função opera em 3 ações fundamentais distintas:
    # 1)faz a requisição de uma pagina, pesquisa, extrai e armaneza os dados na lista global.
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_grid = soup.find_all('li', attrs={"class" : "promotion-item"})
    for prod in product_grid:
        preco_atual = prod.find('span', attrs={"class" : "promotion-item__price"})
        reais = preco_atual.find('span').text
        if preco_atual.find('sup') is None: 
            centavos = '' 
        else: 
            centavos = ", " + preco_atual.find('sup').text
        data_dicts.append(
            {
            "nome-produto" : prod.find('p', attrs={"class" : "promotion-item__title"}).text,
            "preco-antigo" : prod.find('span', attrs={"class" : "promotion-item__oldprice"}).text,
            "preco-atual" : reais + centavos,
            "link-produto" : prod.find('a', attrs={"class" : "promotion-item__link-container"}).get('href')
            }
        )
    # 2)Pesquisa por um seletor presente em todas as páginas exceto na última.
    is_nextpage = soup.find('li', attrs={'class' : 'andes-pagination__button andes-pagination__button--next'})
    if is_nextpage:
        # 3)Enquanto achar esse seletor, obtem o URL da proxima página e repete os passos 1 e 2 por recursão.
        url = is_nextpage.a.get('href') #notação de ponto para acessar a tag a
        pageScraper(url, data_dicts)
    return data_dicts


def main():
    data_dicts = list()
    url = "https://www.mercadolivre.com.br/ofertas?page=1" # URL da 1ª página da seção de ofertas.
    database = pageScraper(url, data_dicts)

    # por fim converter a lista de dicts para um pandas DF e exportar a base
    dfexp = pd.DataFrame(database)
    dfexp.to_csv('database-ofertas-ML.csv')
    # talvez esse último passo possa ser melhorado com modulo csv
    # Caso positivo, um CSV com o titulo acima será criado no diretório local.

main()#run forest, run 