import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

dados=[]
num =1
navegador = webdriver.Chrome()
navegador.get('https://www.99freelas.com.br/projects?p=f')
while num <101:
    num+=1
    site = BeautifulSoup(navegador.page_source, 'html.parser')
    sleep(0.7)
    propostas = site.findAll('li', attrs={'class':'result-item'})
    for proposta in propostas:
        habilidade = proposta.find('p', attrs={'class': 'item-text habilidades'})
        habilidade = proposta.findAll('a', attrs={'class': 'habilidade'})
        habilidade = ' , '.join([detalhe.text for detalhe in habilidade])
        #print(proposta['data-nome'])
        #print('habilidade: {}'.format(habilidade))
        #print('\n\n\n')
        dados.append([proposta['data-nome'],habilidade])
    navegador.get('https://www.99freelas.com.br/projects?page={}'.format(num))
    
df = pd.DataFrame(dados, columns=['titulo', 'requisitos'])
df.to_excel("planilha.xlsx", index=False)