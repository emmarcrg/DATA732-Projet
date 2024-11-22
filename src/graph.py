from analyse_json_metadata import *
from itertools import islice
from analyse_json_data import *
from collections import defaultdict 
from itertools import combinations

def normaliser_nom(nom):
    #Permet d'éviter certaines répétition : ne fonctionne certainement que pour quelques valeurs, il y a certainement des oublis dans la liste
    normalisation = {
        'Zelensky': 'Volodymyr Zelensky',
        'Macron': 'Emmanuel Macron',
        'Président russe': 'Vladimir Poutine',  # Ajouter des normalisations pour d'autres doublons connus
        'Poutine': 'Vladimir Poutine',
        'Président ukrainien':'Volodymyr Zelensky',
        'Biden':'Joe Biden'
    }
    return normalisation.get(nom, nom)


# On récupère les n personnes les plus influentes
def pers_importantes(n):
    #On récpère les données : la liste de toutes les personnes citées
    data = analyse_kw('data/fr.sputniknews.africa--20220630--20230630.json', 'per')
    
    # Trier le dictionnaire par ses clés dans l'ordre décroissant
    sorted_data = dict(sorted(data.items(), reverse=True))

    # On fait en sorte qu'il n'y ait pas de répétion/ que les données soient cool :
    # Je sais que c'est pas beau mais au moins c'est fait
    filtered_data = {normaliser_nom(v): k for k, v in sorted_data.items() if 'August' not in v 
                     and 'August 12' not in v and 'Président' not in v 
                     and '© Sputnik' not in v and 'Washington' not in v
                     and 'Wagner' not in v}
    
    #On sélectiuonne les 20 personnes les plus influentes
    data_most = dict(islice(filtered_data.items(), n))
    return data_most

#print(pers_importantes(10))   => retourne les données sous la forme personne : apparition

#On récupère la liste des chaînes de caractères 
def get_noms():
    data=pers_importantes(20)
    pers=[]
    
    for personne,cle  in data.items() : 
        pers.append(personne)
    return pers

#print(get_noms()) => retourne le nom des 20 première personnes les plus citées

# On regarde maintenant qui apparaît le plus avec qui : les différents liens entre les personnes
def get_relations():
    data=pd.read_json("data/fr.sputniknews.africa--20220630--20230630.json").get('data')
    print(data)
    pers=get_noms()
    links_count = defaultdict(int) #type de dictionnaire qui remplie si jamais il n'y a pas de valeurs
    
    for year in (2022, 2023):      #C'est pas beau mais on ne prend pas les même mois donc tant pis   
        if(year==2022):
            for month in (7,12): 
                if month==7:
                    for day in (20,31): 
                        # Récupérer les articles pour la date actuelle 
                        articles = recuperer_articles_par_date(data, year, month, day) 
                        pers_day=[]
                        for article in articles :
                            pers_day=recuperer_personnes_par_article(article)
                        people_in_entry=[]
                        print(pers_day)
                        if pers_day is not None:
                            for person in pers_day :
                                if person in pers:
                                    people_in_entry.append(person)
                    
                        # Créer toutes les combinaisons possibles de personnes 2 à 2 
                        for person1, person2 in combinations(people_in_entry, 2): 
                            links_count[(person1, person2)] += 1 
                                
                if month==8 or month==10 or month==12:
                    for day in (1,31): 
                        # Récupérer les articles pour la date actuelle 
                        articles = recuperer_articles_par_date(data, year, month, day) 
                        pers_day=[]
                        for article in articles :
                            pers_day=recuperer_personnes_par_article(article)
                        people_in_entry=[]
                        print(pers_day)
                        if pers_day is not None:
                            for person in pers_day :
                                if person in pers:
                                    people_in_entry.append(person)
                    
                        # Créer toutes les combinaisons possibles de personnes 2 à 2 
                        for person1, person2 in combinations(people_in_entry, 2): 
                            links_count[(person1, person2)] += 1 
                                
                if month==9 or month==11:
                    for day in (1,30): 
                        # Récupérer les articles pour la date actuelle 
                        articles = recuperer_articles_par_date(data, year, month, day) 
                        pers_day=[]
                        for article in articles :
                            pers_day=recuperer_personnes_par_article(article)
                        people_in_entry=[]
                        print(pers_day)
                        if pers_day is not None:
                            for person in pers_day :
                                if person in pers:
                                    people_in_entry.append(person)
                    
                        # Créer toutes les combinaisons possibles de personnes 2 à 2 
                        for person1, person2 in combinations(people_in_entry, 2): 
                            links_count[(person1, person2)] += 1 
                                
        if (year==2023):
            for month in (1,6): #On ne prend pas en compte le mois de juin : les données se terminent le 
                if month==1 or month==3 or month==5:
                    for day in (1,31): 
                        # Récupérer les articles pour la date actuelle 
                        articles = recuperer_articles_par_date(data, year, month, day) 
                        pers_day=[]
                        for article in articles :
                            pers_day=recuperer_personnes_par_article(article)
                        people_in_entry=[]
                        print(pers_day)
                        if pers_day is not None:
                            for person in pers_day :
                                if person in pers:
                                    people_in_entry.append(person)
                    
                        # Créer toutes les combinaisons possibles de personnes 2 à 2 
                        for person1, person2 in combinations(people_in_entry, 2): 
                            links_count[(person1, person2)] += 1 
                                
                if month==4:
                    for day in (1,30): 
                        # Récupérer les articles pour la date actuelle 
                        articles = recuperer_articles_par_date(data, year, month, day) 
                        pers_day=[]
                        for article in articles :
                            pers_day=recuperer_personnes_par_article(article)
                        people_in_entry=[]
                        print(pers_day)
                        if pers_day is not None:
                            for person in pers_day :
                                if person in pers:
                                    people_in_entry.append(person)
                    
                        # Créer toutes les combinaisons possibles de personnes 2 à 2 
                        for person1, person2 in combinations(people_in_entry, 2): 
                            links_count[(person1, person2)] += 1 
                if month==2:
                    for day in (1,28): 
                        # Récupérer les articles pour la date actuelle 
                        articles = recuperer_articles_par_date(data, year, month, day) 
                        pers_day=[]
                        for article in articles :
                            pers_day=recuperer_personnes_par_article(article)
                        people_in_entry=[]
                        print(pers_day)
                        if pers_day is not None:
                            for person in pers_day :
                                if person in pers:
                                    people_in_entry.append(person)
                    
                        # Créer toutes les combinaisons possibles de personnes 2 à 2 
                        for person1, person2 in combinations(people_in_entry, 2): 
                            links_count[(person1, person2)] += 1 
                if month==6:
                    for day in (1,29): 
                        # Récupérer les articles pour la date actuelle 
                        articles = recuperer_articles_par_date(data, year, month, day) 
                        pers_day=[]
                        for article in articles :
                            pers_day=recuperer_personnes_par_article(article)
                        people_in_entry=[]
                        print(pers_day)
                        if pers_day is not None:
                            for person in pers_day :
                                if person in pers:
                                    people_in_entry.append(person)
                    
                        # Créer toutes les combinaisons possibles de personnes 2 à 2 
                        for person1, person2 in combinations(people_in_entry, 2): 
                            links_count[(person1, person2)] += 1 
                                
                                
    return links_count 
# Appeler la fonction et obtenir les résultats 
rel=get_relations() 
for relation, lien in rel.items() :
    print(str(relation) + " ont " + str(lien))
# On met les données sous la bonne forme 

'''
Pour faire des graphes sous python : 
- plotly Graph object
- https://plotly.com/python/network-graphs/
'''