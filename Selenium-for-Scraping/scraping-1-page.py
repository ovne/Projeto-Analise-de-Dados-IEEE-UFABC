""" OBJETIVO: Utilizar a API python-selenium para requisitar, interagir e raspgar 
dados de uma página web.
"""

from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://www.mercadolivre.com.br/ofertas?page=1")

