import pandas as pd
import numpy as np
import requests as r
import re
import sys

#Ce script lie le .csv créé par scrap.py et le parcourt
#On prend des arguments de l'exe pour voir quelle zone du dataframe on parcourt

#python cond.py 10 23

name_df = 'linked_url_test.csv'

deb = int(sys.argv[1]) #Indice à partir duquel on lit le dataframe >=1
length = int(sys.argv[2]) #Nombres de lignes lues

#On doit avoir la ligne d'en-tête avec le nom des colonnes
df = pd.read_csv(name_df, skiprows=range(1, deb), nrows=length)

#Renvoie le code html de la page pointée par l'url
def get_page_text_from_url(url_card) :
    html_request = r.get(url_card)
    #URL request get refused
    #assert(str(html_request)=="<Response [200]>")
    if(str(html_request)!="<Response [200]>") :
        print("error : no reponse 200 html request : " + url_card)
        return "error"
    return html_request.text

#print(get_set_from_page(get_page_text_from_url("https://en.play-in.com/rachat/magic/result.php?i=4217")))

#Retourne à partir de l'url_PLAYIN et d'un set, une liste de tous les quadruplets
#(langue, état, foil, prix)
#langue : 1 en / 2 fr
#état : mint 1 / nmint 2 / ex 3 / good 4 / lightplayed 5 / played 6 / poor 7
#foil : N / Y
#prix : float
#Retourne également un set de tuple avec uniquement les paramètres (langue, foil)
def load_parameters_playin(url_PI, set_PI) :
    page = get_page_text_from_url(url_PI)
    sets = r'<img src="/img/extension/symbole_extension/\d*.png" title="([ :&\w]*)" [ \S]*<div class="tr price price_mobile">'
    blocs = r'<select class="[_ \w]*" id="select_[\d]*" data-variation="\d*">(<option data-id="\d*" data-prix="\d*" data-foil="[NO]">[ \S]*</option>)*'

    for index, ext in enumerate(re.compile(sets).findall(page)) :
        if ext == set_PI :
            data = re.compile(blocs).findall(page)[index]
            nuplets = r'<option data-id="\d*" data-prix="(\d*)" data-foil="([NO])">(Fr|En) ([ /\w]*)</option>'
            output_pre = re.compile(nuplets).findall(data)

            #Remise au bon format de la liste de tuple
            output_list = []
            for output in output_pre :
                tlan = output[2]
                tetat = output[3]
                tfoil = output[1]
                tprix = output[0]

                if tlan == 'Fr' :
                    tlan = 2
                elif tlan == 'En' :
                    tlan = 1

                if tetat == 'Mint/Nmint' :
                    tetat = 2
                elif tetat == 'Exc' :
                    tetat = 3
                elif tetat == 'Fine' :
                    tetat = 4
                elif tetat == 'Played' :
                    tetat = 6
                elif tetat == 'Poor' :
                    tetat = 7

                if tfoil == 'O' :
                    tfoil = 'Y'

                tprix = float(tprix)

                output_list.append((tlan, tetat, tfoil, tprix))

            output_set = set()

            for output in output_list :
                output_set.add((output[0], output[2]))

            return output_list, output_set

#print(load_parameters_playin("https://en.play-in.com/rachat/magic/result.php?i=8298","Ice Age"))

#Retourne à partir de l'url_CM et d'un quadruplet de conditions ci-dessus
#l'url de la page cardmarket afin de récupérer via une autre fonction les opportunités
#On ne considère que les professionnels et les powersellers
#On ne considère que les vendeurs français (délais de livraison)
#On ne regarde pas la qualité (traitée plus tard), car on regarde toutes les cartes de qualité supérieure ou égale
def get_url_parameters_cardmarket(url_CM, nuplet) :
    return url_CM + "?sellerCountry=12&sellerType=1,2&language=" + str(nuplet[0]) + "&isFoil=" + str(nuplet[1])

#Retourne une liste de nuplets avec (nom_vendeur, état, quantité, prix)
def get_list_price_cardmarket(url_CM) :
    page = get_page_text_from_url(url_CM).replace("'",'"').replace("(","\(").replace(")","\)").replace(".","\.")
    #l'url du vendeur est https://cardmarket.com/en/Magic/Users/name
    vendeur = r'<span class="d-flex has-content-centered mr-1"><a href="/en/Magic/Users/([-\w]*)">'
    etat = r'<span class="badge ">(\w*)</span>'
    quantite = r'<div class="amount-container d-none d-md-flex justify-content-end mr-3"><span class="item-count small text-right">(\d*)</span>'
    prix = r'<span class="font-weight-bold color-primary small text-right text-nowrap">([,\d]*) €</span></div></div></div></div></div>'

    vendeur = re.compile(vendeur).findall(page)
    etat = re.compile(etat).findall(page)
    quantite = re.compile(quantite).findall(page)
    prix = re.compile(prix).findall(page)

    # print(len(vendeur))
    # print(len(etat))
    # print(len(quantite))
    # print(len(prix))

    if not(len(vendeur) == len(etat) == len(quantite) == len(prix)) :
        print("error : size data extracted from cm inconsistent")

    output = []
    for i in range(len(vendeur)) :
        if(etat[i]=='M') :
            etat[i] = 1
        if(etat[i]=='NM') :
            etat[i] = 2
        if(etat[i]=='EX') :
            etat[i] = 3
        if(etat[i]=='GD') :
            etat[i] = 4
        if(etat[i]=='LP') :
            etat[i] = 5
        if(etat[i]=='PL') :
            etat[i] = 6
        if(etat[i]=='PO') :
            etat[i] = 7           
        output.append((vendeur[i], etat[i], quantite[i], prix[i]))
    return output

#Analyse si une offre d'achat est potentiellement intéressante à l'achat
def is_rentable(nupplet_offre, nupplet_PI) :
    #A COMPLETER
    return False

nuplet_test = ("1", "4", "N", 32)



def analyse(df) :

    output_df = pd.DataFrame({
        'nom_vendeur': [],
        'etat': [],
        'quantite': [],
        'prix_CM': [],
        'prix_PI': [],
        'language': [],
        'foil': [],
        'url_CM': [],
        'url_PI': []
        })

    #On parcourt le df selon un couple (set,url_PI)
    for index,row in df.iterrows() :
        list_nuplet_parameters, set_nuplet = load_parameters_playin(row.url_PI, row.set_PI)
        #On parcourt la liste des combinaisons d'achat
        for tuplet in set_nuplet :
            url_CM = get_url_parameters_cardmarket(row.url_CM, tuplet)
            #print(url_CM)
            correspond = get_list_price_cardmarket(url_CM)
            #On parcourt les offres correspondantes de cardmarket
            #On compare bien l'état pour n'avoir que des offres avec qualité similaire
            for nuplet in list_nuplet_parameters :
                for offer in correspond :
                    if(nuplet[1]==offer[1]) :
                        #On regarde si certaines sont intéressantes et on les mets dans un nouveau dataframe
                        if is_rentable(offer, nuplet) :
                            new_row = pd.DataFrame({
                                'nom_vendeur': [offer[0]],
                                'etat': [nuplet[1]],
                                'quantite': [offer[2]],
                                'prix_CM': [offer[3]],
                                'prix_PI': [nuplet[3]],
                                'language': [nuplet[0]],
                                'foil': [nuplet[2]],
                                'url_CM': [url_CM],
                                'url_PI': [row.url_PI]
                                })
                            output_df = pd.concat([output_df, new_row]).reset_index(drop=True)

    return output_df

occas = analyse(df)
occas.to_csv("occas.csv", index=False)
print(occas)


#print(type(nuplet_test))

#print(df.iloc[0].url_CM)

#print(df)

#for url in df.url_CM :
#    print(get_url_parameters_cardmarket(url,nuplet_test))

#print(df)