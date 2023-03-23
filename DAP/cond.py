import pandas as pd
import numpy as np
import requests as r
import re
import sys

#Ce script lie le .csv créé par scrap.py et le parcourt
#On prend des arguments de l'exe pour voir quelle zone du dataframe on parcourt

#python cond.py 10 23

name_df = 'linked_url.csv'

deb = int(sys.argv[1]) #Indice à partir duquel on lit le dataframe
length = int(sys.argv[2]) #Nombres de lignes lues

df = pd.read_csv(name_df, skiprows=range(0, deb), nrows=length)

#Renvoie le code html de la page pointée par l'url
def get_page_text_from_url(url_card) :
    html_request = r.get(url_card)
    #URL request get refused
    #assert(str(html_request)=="<Response [200]>")
    if(str(html_request)!="<Response [200]>") :
        print("error")
        return "error"
    return html_request.text

#Retourne à partir de l'url_PLAYIN et d'un set, une liste de tous les quadruplets
#(langue, état, foil, prix)
#langue : 1 en / 2 fr
#état : nmint 2 / ex 3 / good 4 / lightplayed 5 / played 6 / poor 7
#foil : N / Y
#prix : float
def load_parameters_playin(url_PI, set) :
    #A COMPLETER
    nuplet_test = ("1", "4", "Y", 32)
    return [nuplet_test]

#Retourne à partir de l'url_CM et d'un quadruplet de conditions ci-dessus
#l'url de la page cardmarket afin de récupérer via une autre fonction les opportunités
#On ne considère que les professionnels et les powersellers
#On ne considère que les vendeurs français (délais de livraison)
def get_url_parameters_cardmarket(url_CM, nuplet) :
    return url_CM + "?sellerCountry=12&sellerType=1,2&language=" + nuplet[0] + "&minCondition=" + nuplet[1] + "&isFoil=" + nuplet[2]

#Retourne une liste de nuplets avec (nom_vendeur, état, quantité, prix)
def get_list_price_cardmarket(url_CM) :
    page = get_page_text_from_url(url_CM).replace("'",'"').replace("(","\(").replace(")","\)").replace(".","\.")
    #l'url du vendeur est https://cardmarket.com/en/Magic/Users/name
    vendeur = r'<span class="d-flex has-content-centered mr-1"><a href="/en/Magic/Users/([-\w]*)">'
    etat = r'<span class="badge ">(\w*)</span>'
    quantite = r'<span class="item-count small text-right">(\d*)</span>'
    prix = r'<span class="font-weight-bold color-primary small text-right text-nowrap">([,\d]*) €</span></div></div></div></div></div>'

    vendeur = re.compile(vendeur).findall(page)
    etat = re.compile(etat).findall(page)
    quantite = re.compile(quantite).findall(page)
    prix = re.compile(prix).findall(page)

    output = []
    for i in range(len(vendeur)) :
        output.append((vendeur[i],etat[i],quantite[i],prix[i]))
    return output

#Analyse si une offre d'achat est potentiellement intéressante à l'achat
def rentable(nupplet_offre, nupplet_PI) :
    #A COMPLETER
    return False

nuplet_test = ("1", "4", "N", 32)



def analyse(df) :

    output_df = pd.DataFrame({
        'nom_vendeur': [],
        'quantite': [],
        'prix_livraison': [],
        'prix_CM': [],
        'prix_PI': [],
        'url_CM': [],
        'url_PI': []
        })

    #On parcourt le df selon un couple (set,url_PI)
    for index,row in df.iterrows() :
        list_nuplet_parameters = load_parameters_playin(row.url_PI, row.set)
        #On parcourt la liste des combinaisons d'achat
        for nuplet in list_nuplet_parameters :
            url_CM = get_url_parameters_cardmarket(row.url_CM, nuplet)
            correspond = get_list_price_cardmarket(url_CM)
            #On parcourt les offres correspondantes de cardmarket
            for offer in correspond :
                #On regarde si certaines sont intéressantes et on les mets dans un nouveau dataframe
                if rentable(offer, nuplet) :
                    new_row = pd.DataFrame({'nom_vendeur': [turl_PI], 'name': [tname], 'set': [tset], 'url_CM': [turl_CM]})
                    output_df = pd.concat([output_df, new_row]).reset_index(drop=True)

    return output_df

print((get_list_price_cardmarket("https://www.cardmarket.com/en/Magic/Products/Singles/Jumpstart/Linvala-Keeper-of-Silence?sellerCountry=12&sellerType=1,2&language=1&minCondition=4&isFoil=N")))

#print(type(nuplet_test))

#print(df.iloc[0].url_CM)


for url in df.url_CM :
    print(get_url_parameters_cardmarket(url,nuplet_test))

#print(df)