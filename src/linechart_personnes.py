import pandas as pd
import plotly.graph_objects as go
from analyse_json_metadata import *
import plotly.colors

def normaliser_nom(nom):
    normalisation = {
        'Zelensky': 'Volodymyr Zelensky',
        'Macron': 'Emmanuel Macron',
        'Président russe': 'Vladimir Poutine',  # Ajouter des normalisations pour d'autres doublons connus
        'Président': 'Emmanuel Macron',
        'Poutine': 'Vladimir Poutine'
    }
    return normalisation.get(nom, nom)

def afficher_linechart_personnes():
    print("Chargement du linechart des personnes en cours")
    
    # Créer un dictionnaire pour stocker les données par mois
    data_by_month = {}
    for annee, mois in [(2022, m) for m in range(8, 13)] + [(2023, m) for m in range(1, 7)]:  # Ajouter les mois de 2023 jusqu'à juin
        raw_data = analyse_kw_mois('data/fr.sputniknews.africa--20220630--20230630.json', annee, mois, 'per')
        
        # Filtrer les clés 
        filtered_data = {normaliser_nom(v): k for k, v in raw_data.items() if 'August' not in v 
                        and 'August 12' not in v and 'Président' not in v 
                        and '© Sputnik' not in v and 'Washington' not in v
                        and 'Wagner' not in v}
        
        # Agréger les occurrences des noms normalisés
        aggregated_data = {}
        for personne, occurrence in filtered_data.items():
            if personne in aggregated_data:
                aggregated_data[personne] += occurrence
            else:
                aggregated_data[personne] = occurrence
        
        # Trier les données et ne garder que les 5 plus mentionnées
        sorted_data = dict(sorted(aggregated_data.items(), key=lambda item: item[1], reverse=True)[:5])
        data_by_month[f"{annee}-{mois:02d}"] = sorted_data

    # Convertir les données en DataFrame
    df = pd.DataFrame(data_by_month).fillna(0).T

    # Convertir toutes les colonnes en type numérique (si nécessaire)
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Palette de couleurs distinctes (une couleur par colonne/personne)
    unique_colors = plotly.colors.qualitative.Plotly  # Utilise une palette qualitative par défaut
    color_map = {colonne: unique_colors[i % len(unique_colors)] for i, colonne in enumerate(df.columns)}

    # Créer un diagramme en barres empilées avec Plotly
    fig = go.Figure()
    for colonne in df.columns:
        fig.add_trace(go.Bar(
            x=df.index,
            y=df[colonne],
            name=colonne,
            marker=dict(color=color_map[colonne])  # Appliquer la couleur unique
        ))

    # Mettre à jour la disposition
    fig.update_layout(
        barmode='stack',
        title='Diagramme en barres empilées des Personnes par Mois',
        xaxis_title='Mois',
        yaxis_title='Valeurs',
        xaxis_tickangle=45,
        legend_title='Personnes',
        margin=dict(l=40, r=40, t=40, b=100),
        height=600,
        width=1000
    )

    return fig
