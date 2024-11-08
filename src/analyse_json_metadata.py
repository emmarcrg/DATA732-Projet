import json

def analyse_kw (data) :
    #Récupérer les kws qui se trouvent dans all
    # Charger le fichier JSON
    with open(data, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Récupérer les éléments dans 'kws'
    kws_elements = data["metadata"]["all"]["kws"]

    # Inverser le dictionnaire: clé devient valeur, valeur devient clé
    kws_inverted = {value: key for key, value in kws_elements.items()}

    # Afficher le dictionnaire inversé
    print(kws_inverted)

    pass    

    
def analyse_locs () :
    #
    pass

def analyse_org () :
    #
    pass

def analyse_per () :
    #
    pass

def analyse_mis () :
    #
    pass

analyse_kw('data/fr.sputniknews.africa--20220630--20230630.json')