
'''
OBJETIVO: Utilizar as bliotecas requests e BeautifulSoup para fazer a requisição
e extrair alguns dados de uma única página HTML.
'''


import requests
from bs4 import BeautifulSoup
import pandas as pd


link = "https://www.mercadolivre.com.br/ofertas#nav-header"
# 1-requisição
response = requests.get(link)
# checando se está ok
print(response.status_code)
#atribuindo o conteudo da página
html = response.content
# 2-Instanciando objeto BS e HTML parser
soup = BeautifulSoup(html, 'html.parser')
# 3-find_all() vai buscar em todo o conteúdo pelas tags e atributos html passados.
goods = soup.find_all('li', attrs={"class" : "promotion-item"})

data = []
# 4-Vou passar por esses pedaços de página e extrair os dados de interesse
for product in goods:
    data.append(
        {
            "produto" : product.find('p', attrs={"class" : "promotion-item__title"}).text,
            "preco-antigo" : product.find('span', attrs={"class" : "promotion-item__oldprice"}).text,
            "preco-atual" : product.find('span', attrs={"class" : "promotion-item__price"}).text,
            "link" : product.find('a', attrs={"class" : "promotion-item__link-container"}).get('href')
        }
    )

# aparentemente, deu muito bom :D 
# agora, vou converter essa lista de dicionários em um DF pandas
dfproducts = pd.DataFrame(data, index=None)
# por fim vou arquivar em um arquico CSV
dfproducts.to_csv('raspagem-teste01.csv')
# Caso positivo, um CSV com o título acima sera criado no mesmo diretório.

print(dfproducts)