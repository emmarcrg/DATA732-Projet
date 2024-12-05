import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
from analyse_json_metadata import analyse_kw_mois  # data, année, mois, type

fichier_data = "data/fr.sputniknews.africa--20220630--20230630.json"

def axe_x(fichier_data):
    data_month = pd.read_json(fichier_data).get('metadata').get('month')
    # Mois de l'année 2022 :
    annee2022 = sorted([int(mois) for mois in data_month['2022'].keys()])
    mois2022 = [f"{mois} - 2022" for mois in annee2022]
    # Mois de l'année 2023 :
    annee2023 = sorted([int(mois) for mois in data_month['2023'].keys()])
    mois2023 = [f"{mois} - 2023" for mois in annee2023]
    
    valeurs_x = mois2022 + mois2023
    return valeurs_x, annee2022, annee2023

def occurrences_organisation_par_mois(fichier_data, annee2022, annee2023, valeurs_x):
    occurrences_par_mois = defaultdict(lambda: defaultdict(int))
    for i, mois in enumerate(annee2022):
        liste_organisations = analyse_kw_mois(fichier_data, 2022, mois, "org")
        for nb_occurrences, orga in liste_organisations.items():
            occurrences_par_mois[valeurs_x[i]][orga] += nb_occurrences
    for i, mois in enumerate(annee2023):
        liste_organisations = analyse_kw_mois(fichier_data, 2023, mois, "org")
        for nb_occurrences, orga in liste_organisations.items():
            occurrences_par_mois[valeurs_x[i + len(annee2022)]][orga] += nb_occurrences
    return occurrences_par_mois

def tri_organisation_par_mois(occurrences_par_mois, taille):
    for mois, organisations in occurrences_par_mois.items():
        liste_triee = sorted(organisations.items(), key=lambda x: x[1], reverse=True)
        occurrences_par_mois[mois] = liste_triee[:taille]
    return occurrences_par_mois

def graphique_bubble_chart(valeurs_x, occurrences_par_mois):
    x_vals, y_vals, z_vals = [], [], []

    for mois, organisations in occurrences_par_mois.items():
        for org, occurrences in organisations:
            x_vals.append(mois)
            y_vals.append(org)
            z_vals.append(occurrences)

    # Échelle des tailles
    size_factor = 5  # Ajuster pour réduire les tailles des bulles
    scaled_sizes = [size_factor * (val ** 0.5) for val in z_vals]  # Échelle racine carrée pour équilibrer les tailles

    # Création du graphique bubble chart
    fig = go.Figure(data=[go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='markers',
        marker=dict(
            size=scaled_sizes,
            color=z_vals,
            colorscale='Viridis',
            showscale=True,  # Activer l'échelle des couleurs
            colorbar=dict(
                title="Occurrences",
                titleside="right"
            ),
            opacity=0.7,
            line=dict(width=1, color='black')
        )
    )])

    # Mise en page
    fig.update_layout(
        title="Occurrences des Organisations par Mois",
        xaxis_title="Mois",
        yaxis_title="Organisations",
        xaxis=dict(tickangle=45),  # Améliorer la lisibilité des ticks
        height=600,
        width=1000
    )
    fig.show()
    return fig

def afficher_bubblechart():
    print("Chargement du bubblechart en cours")
    valeurs_x, annee2022, annee2023 = axe_x(fichier_data)
    occurrences = occurrences_organisation_par_mois(fichier_data, annee2022, annee2023, valeurs_x)
    occurrences_par_mois = tri_organisation_par_mois(occurrences, 5)
    fig = graphique_bubble_chart(valeurs_x, occurrences_par_mois)
    return fig

afficher_bubblechart()