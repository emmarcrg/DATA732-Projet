import pandas as pd

data=pd.read_json("data/fr.sputniknews.africa--20220630--20230630.json").get('data')
#print(data.head())

def recuperer_articles_par_date(data, annee, mois, jour):
    """Récupère les articles qui ont été publiés à une date donnée
    Début le 20 juillet 2022 : 2022 7 20
    Fin le 29 juin 2023
    Input : - fichier data
            - annee : un nombre 
            - mois : un nombre sans le 0 devant (ex : janvier=1, fevrier=2...)
            - jour : un nombre sans le 0 devant
    Output : une liste d'articles"""
    annee=str(annee)
    mois=str(mois)
    jour=str(jour)
    liste_articles_date=data.get(annee, {}).get(mois, {}).get(jour, None)
    return liste_articles_date

def recuperer_noms_articles(liste_articles):
    """Récupère les noms des articles d'une liste d'articles donnée
    Input : une liste d'article
    Output : un dictionnaire des noms des articles
    """    
    liste_noms_articles=[]
    for article in liste_articles:
        liste_noms_articles.append(article.get('title'))
    return liste_noms_articles    


def recuperer_occurence_personnes_par_article(article):
    """Récupère le nombre d'appartition des personnes citées dans l'article donné"""
    liste_personnes=article.get('per', None)
    if liste_personnes :
        return liste_personnes
    else :
        return None
    
def recuperer_personnes_par_article(article):
    """Récupère les personnes citées dans l'article donné sous forme de liste"""
    liste_personnes=article.get('per', None)
    personnes=[]
    for personne in liste_personnes :
        personnes.append(personne)
    
    if personnes :
        return personnes
    else :
        return None




###### TEST ######
'''
print("\nRécupération des articles du 28 mars 2023")
liste_articles=recuperer_articles_par_date(data, "2023", "3", "28")
print("Nombre d'articles : ", len(liste_articles))
noms_articles=recuperer_noms_articles(liste_articles)
for nom in noms_articles :
    print(" - ", nom)
"""On récupère bien la liste des noms articles et ils correspondent à ceux qu'on voit dans Mozilla"""

for article in liste_articles:
    occurence_personnes=recuperer_occurence_personnes_par_article(article)
    personnes=recuperer_personnes_par_article(article)
    print("Occurence : ", occurence_personnes)
    print("Personnes : ", personnes)

"""On récupère bien les personnes pour chaque article avec le nombre d'occurence dans celui-ci"""
'''