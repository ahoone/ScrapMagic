import pandas as pd
import numpy as np
import requests as r
import re
import os

mode_test = False

url_hotlist = "https://en.play-in.com/rachat/hotlist/magic/"
url_CM = "https://www.cardmarket.com/en/Magic/Products/Singles/"

#Renvoie le code html de la page pointée par l'url
def get_page_text_from_url(url_card) :
    html_request = r.get(url_card)
    #URL request get refused
    #assert(str(html_request)=="<Response [200]>")
    if(str(html_request)!="<Response [200]>") :
        return url_hotlist
    return html_request.text

#Retourne le nombre de pages web de la hotlist
def get_num_page_hotlist(url=url_hotlist) :
    page = get_page_text_from_url(url).replace("'",'"')
    num_page = r'<div class="each_page between_page page_not_mobile">...</div>\S* \D*(\d*)'
    return int(re.compile(num_page).findall(page)[0])

#Retourne la liste des index des cartes d'une page de la hotlist
def extract_cards_from_page_url(url) :
    page = get_page_text_from_url(url)
    num_card = r'<a href="/rachat/magic/result.php\Wi=(\d*)">'
    return re.compile(num_card).findall(page)

#Retourne les url de toutes les cartes de la hotlist
def get_all_hotlist_cards_url(url_hotlist=url_hotlist, mode_test=mode_test) :
    output = []
    if(mode_test) :
        for i in range(1,2) :
            for j in extract_cards_from_page_url(url_hotlist+"?p="+str(i)) :
                output.append("https://en.play-in.com/rachat/magic/result.php?i="+j)        
    else :
        for i in range(1,get_num_page_hotlist(url_hotlist)) :
            for j in extract_cards_from_page_url(url_hotlist+"?p="+str(i)) :
                output.append("https://en.play-in.com/rachat/magic/result.php?i="+j)
    return output

#Retourne les sets d'une carte PI qui sont rachetés
#On ne compte pas les différentes versions d'une carte d'une même extension
def get_set_from_page(page) :
    name_set = r'<img src="/img/extension/symbole_extension/\d*.png" title="([ :&\w]*)" [ \S]*<div class="tr price price_mobile">'
    occ = re.compile(name_set).findall(page)

    #Supprimer les problèmes
    output = []
    for i in range(0,len(occ)) :
        verif = True
        for j in range(0,len(occ)) :
            if i!=j and occ[i]==occ[j] :
                verif = False
        if verif :
            output.append(occ[i].replace(":","").replace(" ","-"))

    return output

#Retourne la longest substring from a list of string
#Utilisé pour trouver le nom d'une carte
def findstem(arr) :
	n = len(arr)
	s = arr[0]
	l = len(s)
	res = ""

	for i in range(l):
		for j in range(i + 1, l + 1):
			stem = s[i:j]
			k = 1
			for k in range(1, n):
				if stem not in arr[k]:
					break
			if (k + 1 == n and len(res) < len(stem)):
				res = stem

	return res

#Donne le nom de la carte
def get_card_name_from_page(page) :
    name_card = r'<div class="tr name name_mobile">([ \S]*)</div>\s'
    occ = re.compile(name_card).findall(page)
    #assert(len(occ)!=0)
    #Error in the identification of the name
    #Will be not considered in the DataFrame
    if(len(occ) == 0) :
        return "xxx"
    if(len(occ) == 1) :
        return occ[0].replace(",","").replace("'","").replace("//","").replace("  "," ").replace(" ","-")
    return findstem(occ).replace(",","").replace("'","").replace("//","").replace("  "," ").replace(" ","-")

#Retourne False si la requête url a mené à l'apparition du bouton d'alerte
#Utilisé pour vérifier que l'url supposé n'est pas invalide
#Mais ne permet pas de dire que c'est le bon
def check_url_cm(url_CM) :
    page = get_page_text_from_url(url_CM)
    alert = r'<div class="alert-content"><h4 class="alert-heading">Invalid product!</h4></div></div></div>'
    occ = re.compile(alert).findall(page)
    return not bool(occ)

#Retourne le dataframe url_PI / name / set / url_CM
#Tous les noms (name et set) sont au format pour accéder via requête url à la page CM
#Le champ url_CM contient l'url SUPPOSE de la page CM, possible erreur, notamment à cause des caractères spéciaux
def get_dataframe(test_url_cm=True) :
    df = pd.DataFrame({'url_PI': [], 'name': [], 'set': [], 'url_CM': []})
    print("Assembling all cards_url of PlayIn...", end='\r')
    hotlist = get_all_hotlist_cards_url()
    for percent_card, turl_PI in enumerate(hotlist) :
        page = get_page_text_from_url(turl_PI)
        tname = get_card_name_from_page(page)
        sets = get_set_from_page(page)
        for percent_set, tset in enumerate(sets) :
            print("cartes traitées : " + "{:.2f}".format(percent_card*100/len(hotlist)) + " % | sets de la carte : " + str(percent_set) + "/" + str(len(sets)) + "        ", end='\r')
            turl_CM = url_CM + tset + "/" + tname
            if(test_url_cm and check_url_cm(turl_CM)) :
                #print(turl_PI)
                #print(tname)
                #print(tset)
                #print(turl_CM)
                new_row = pd.DataFrame({'url_PI': [turl_PI], 'name': [tname], 'set': [tset], 'url_CM': [turl_CM]})
                df = pd.concat([df, new_row]).reset_index(drop=True)
            else :
                new_row = pd.DataFrame({'url_PI': [turl_PI], 'name': [tname], 'set': [tset], 'url_CM': [turl_CM]})
                df = pd.concat([df, new_row]).reset_index(drop=True)
    return df

df = get_dataframe()
df.to_csv('linked_url.csv', index=False)
print(df)


#print(get_all_hotlist_cards_url())

#print(check_url_cm("https://www.cardmarket.com/en/Magic/Products/Singles/Dragons-of-Tarkir/1"))

#print(get_card_name_from_page(get_page_text_from_url("https://en.play-in.com/rachat/magic/result.php?i=19233")))
#print(get_set_from_page(get_page_text_from_url("https://en.play-in.com/rachat/magic/result.php?i=19233")))