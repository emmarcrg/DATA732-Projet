import json

def analyse_kw (data, type) :
    #Récupérer les données type qui se trouvent dans all
    #data = le fichier json, type = kws, loc, per, org etc.
    
    # Charger le fichier JSON
    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Récupérer les éléments dans 'kws'
    kws_elements = data["metadata"]["all"][type]

    # Inverser le dictionnaire: clé devient valeur, valeur devient clé
    kws_inverted = {value: key for key, value in kws_elements.items()}

    # Afficher le dictionnaire inversé
    #print(kws_inverted)
    return kws_inverted
    
def analyse_kw (data, annee, type) :
    #Récupérer les données  type en fonction de l'année
    '''data = le fichier json
    type = kws, loc, per, org etc.
    annee int de l'année (2022 ou 2023)'''
    
    # Charger le fichier JSON
    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Récupérer les éléments dans 'kws'
    kws_elements = data["metadata"]["year"][str(annee)][type]

    # Inverser le dictionnaire: clé devient valeur, valeur devient clé
    kws_inverted = {value: key for key, value in kws_elements.items()}

    # Afficher le dictionnaire inversé
    #print(kws_inverted)
    return kws_inverted
    
def analyse_kw (data, annee, mois, type) :
    #Récupérer les données  type en fonction de l'année
    '''data = le fichier json
    type = kws, loc, per, org etc.
    annee int de l'année (2022 ou 2023),
    mois int du mois 2022 : de 7 à 12 et 2023 : de 1 à 6'''
    
    # Charger le fichier JSON
    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Récupérer les éléments dans 'kws'
    kws_elements = data["metadata"]["month"][str(annee)][str(mois)][type]

    # Inverser le dictionnaire: clé devient valeur, valeur devient clé
    kws_inverted = {value: key for key, value in kws_elements.items()}

    # Afficher le dictionnaire inversé
    print(kws_inverted)
    return kws_inverted
    
######## TEST 1 : dans le all, fonctionne avec kws et loc
#analyse_kw('data/fr.sputniknews.africa--20220630--20230630.json', 'loc')

######## TEST 2 : on rajoute year, fonctionne avec per en 2023 et loc en 2022
#analyse_kw('data/fr.sputniknews.africa--20220630--20230630.json',2023, 'per')

######## TEST 3 : on rajoute month, fonctionne avec per en 3/2023 et org en 10/2022
analyse_kw('data/fr.sputniknews.africa--20220630--20230630.json',2022, 10, 'org')

######## TEST 4 : on rajoute day, fonctionne avec per en 2023 et loc en 2022
#analyse_kw('data/fr.sputniknews.africa--20220630--20230630.json',2023, 'per')