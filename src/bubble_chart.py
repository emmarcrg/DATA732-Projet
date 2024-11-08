import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
from analyse_json_metadata import analyse_kw_mois #data, année, mois, type

fichier_data="data/fr.sputniknews.africa--20220630--20230630.json"
# on va faire un Bubble chart de l'occurence de des organisations par mois de publication des articles.

# on récupère la liste des mois à traiter pour l'axe x
def axe_x(fichier_data):
    data_month=pd.read_json("data/fr.sputniknews.africa--20220630--20230630.json").get('metadata').get('month')
    # mois de l'année 2022 :
    annee2022=[]
    for mois in data_month['2022'].keys() :
        annee2022.append(int(mois))
    annee2022=sorted(annee2022)
    mois2022=[]
    for mois in annee2022 :
        mois2022.append(str(mois)+" - 2022")

    # mois de l'année 2023 :
    annee2023=[]
    for mois in data_month['2023'].keys() :
        annee2023.append(int(mois))
    annee2023=sorted(annee2023)
    mois2023=[]
    for mois in annee2023 :
        mois2022.append(str(mois)+" - 2023")
    
    valeurs_x=mois2022+mois2023
    return valeurs_x, annee2022, annee2023

valeurs_x, annee2022, annee2023=axe_x(fichier_data)

# on récupère la liste des organisations
def axe_y(fichier_data, annee2022, annee2023):
    liste_organisations=[]
    for mois in annee2022 :
        orgas=analyse_kw_mois(fichier_data, 2022, mois, "org")
        for nb, orga in orgas.items():
            liste_organisations.append(orga)

    for mois in annee2023 :
        orgas=analyse_kw_mois(fichier_data, 2023, mois, "org")
        print(orgas)
        for nb, orga in orgas.items():
            liste_organisations.append(orga)
        
    print(liste_organisations)

    # on calcule le nombre d'occurence total pour chaque organisation:
    occurrences_by_org = defaultdict(int)

    # Remplir le dictionnaire avec les sommes des occurrences par organisation
    for nb, org in liste_organisations.items():
        occurrences_by_org[org] += nb

    # Afficher le résultat
    print(occurrences_by_org)
    
    return liste_organisations

valeurs_y=axe_y(fichier_data, annee2022, annee2023)
print(valeurs_y)


fig = go.Figure(data=[go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 11, 12, 13],
    mode='markers',
    marker_size=[40, 60, 80, 100])
])

#fig.show()