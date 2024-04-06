import requests
from bs4 import BeautifulSoup as bs

link = 'http://airfoiltools.com/search/index?MAirfoilSearchForm%5BtextSearch%5D=&MAirfoilSearchForm%5BmaxThickness%5D=18&MAirfoilSearchForm%5BminThickness%5D=8.5&MAirfoilSearchForm%5BmaxCamber%5D=&MAirfoilSearchForm%5BminCamber%5D=&MAirfoilSearchForm%5Bgrp%5D=&MAirfoilSearchForm%5Bsort%5D=11&yt0=Search'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

def main():
    """req = requests.get(link, headers = headers)
    print(req)
    #print(req.text)
    site = bs(req.text, "html.parser")
    #print(site.prettify())
    print(site.find('textarea', class_="gLFyf")['value']) """

    req = requests.get(link, headers = headers)
    site = bs(req.text, "html.parser")
    final_data = {}

    count = 0

    while True:
        #links1 = get_links('Airfoil details', site)
        links2 = get_links('Selig format dat file', site) #lista com links de dados de cada Airfoil da pagina aberta

        data = get_data(links2) #cria um dicionario com key: nome do Airfoil e value: dados
        print(len(data.keys()))
        print(count)

        final_data.update(data) #adiciona o dicionario data em final_data onde estarão todos os dados recolhidos

        next = get_links('Next', site)[0] #pega o link da proxima pagina
        if next == None: #se não houver link quebra while
            break
        #if count >= 5:
            #break
        req = requests.get(next, headers = headers) #faz requisição para proxima pagina
        site = bs(req.text, "html.parser") #atualiza variavel site

        count+= 1

    print(final_data)
    print(final_data.keys())
    print(len(final_data.keys()))

def get_links(n, site):
    links = []
    busca = site.find_all('a')
    for a in busca:
        if n in a.get_text():
            new_link = 'http://airfoiltools.com/' + a['href']
            links.append(new_link)
    return links

def get_data(lista):
    data_dict = {}
    for link in lista:
        airfoil_name = (link.split('='))[1]
        new_req = requests.get(link)
        data_dict[airfoil_name] = new_req.text
    return data_dict

main()
