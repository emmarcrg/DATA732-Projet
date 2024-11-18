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

# on récupère la liste des organisations
def occurrences_organisation_par_mois(fichier_data, annee2022, annee2023, valeurs_X):
    occurrences_par_mois=defaultdict(lambda: defaultdict(int))

    for i, mois in enumerate(annee2022):
        liste_organisations = analyse_kw_mois(fichier_data, 2022, mois, "org")
        for nb_occurrences, orga in liste_organisations.items():
            occurrences_par_mois[valeurs_X[i]][orga] += nb_occurrences # valeurs_X[i] correspond à l'indice du mois pour l'année 2022

    for i, mois in enumerate(annee2023):
        print(mois)
        print(valeurs_X[i+len(annee2022)])
        liste_organisations = analyse_kw_mois(fichier_data, 2023, mois, "org")
        for nb_occurrences, orga in liste_organisations.items():
            occurrences_par_mois[valeurs_X[i+len(annee2022)]][orga] += nb_occurrences #valeurs_X[i+len(annee2022)] correspond à l'indice du mois pour l'année 2023
    print(tri_organisation_par_mois)
    return occurrences_par_mois

def tri_organisation_par_mois(occurrences_par_mois):
    # on trie les organisations par ordre décroissant de fréquence par mois
    for mois, organisations in occurrences_par_mois.items():
        liste_triee=sorted(organisations.items(), key=lambda x: x[1], reverse=True)
        occurrences_par_mois[mois]=liste_triee[:10]
    return occurrences_par_mois


def graphique_bubble_chart(valeurs_x, occurrences_par_mois):
    x_vals=[]
    y_vals=[]
    z_vals=[]

    for mois, organisations in occurrences_par_mois.items():
        for org, occurrences in organisations:
            x_vals.append(mois)
            y_vals.append(org) 
            z_vals.append(occurrences)

    # création du graphique bubble chart : taille des bulles = occurences
    fig = go.Figure(data=[go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers',
        marker=dict(
            size=z_vals,
            color=z_vals,
            colorscale='Viridis',
            opacity=0.7,
            line=dict(width=1, color='black')
        )
    )])

    # mise en page
    fig.update_layout(
        title="Occurrences des Organisations par Mois",
        xaxis_title="Mois",
        yaxis_title="Organisations",
        showlegend=False
    )

    fig.show()

valeurs_x, annee2022, annee2023=axe_x(fichier_data)
occurrences=occurrences_organisation_par_mois(fichier_data, annee2022, annee2023, valeurs_x)
occurrences_par_mois=tri_organisation_par_mois(occurrences)
graphique_bubble_chart(valeurs_x, occurrences_par_mois)
