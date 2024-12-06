import pandas as pd
import plotly.graph_objects as go
from analyse_json_metadata import *
import plotly.colors

def normaliser_nom(nom):
    normalisation = {
        'russes': 'russe',
        'militaires': 'militaire',
    }
    return normalisation.get(nom, nom)


def afficher_linechart_mots():
    print("Chargement du linechart des mots en cours")
    
   # on stocke les données par mois dans un dictionnaire
    data_by_month = {}
    for annee, mois in [(2022, m) for m in range(8, 13)] + [(2023, m) for m in range(1, 7)]:  # pour 2023 on va jusqu'à juin
        print(f"Traitement des données pour {annee}-{mois:02d}...")
        raw_data = analyse_kw_mois('data/fr.sputniknews.africa--20220630--20230630.json', annee, mois, 'kws')
        
        if not raw_data:
            print(f"Erreur: Les données de {annee}-{mois:02d} ne sont pas au format attendu.")
            continue
        
        #print(f"Données brutes pour {annee}-{mois:02d} : {raw_data}")

        # on fait en sorte que le mot soit la clé
        inverted_data={value: key for key, value in raw_data.items()}
        data_normalisee={normaliser_nom(v):k for v, k in inverted_data.items()}

        # on trie par fréquence et on garde les 100 qui apparaissent le plus
        sorted_data = dict(sorted(data_normalisee.items(), key=lambda item: item[1], reverse=True)[:100])
        #print(f"Données triées pour {annee}-{mois:02d} : {sorted_data}")
        
        data_by_month[f"{annee}-{mois:02d}"] = sorted_data

    df = pd.DataFrame(data_by_month).fillna(0).T

    # coulerus
    unique_colors = plotly.colors.qualitative.Plotly 
    color_map = {colonne: unique_colors[i % len(unique_colors)] for i, colonne in enumerate(df.columns)}
    #print(f"Carte des couleurs : {color_map}")

    sorted_columns = df.sum().sort_values(ascending=False).index

    # diagramme en barres empilées avec Plotly
    #print("Création du diagramme...")
    fig = go.Figure()
    for colonne in sorted_columns:
        fig.add_trace(go.Bar(
            x=df.index,
            y=df[colonne],
            name=colonne,
            marker=dict(color=color_map[colonne])
        ))

    #print("Mise à jour de la disposition du graphique...")
    fig.update_layout(
        barmode='stack',
        title='Diagramme en barres empilées des Mots-clés par Mois',
        xaxis_title='Mois',
        yaxis_title='Valeurs',
        xaxis_tickangle=45,
        legend_title='Mots-clés',
        legend=dict(
            title='Mots-clés',
            orientation='v',
            x=1,
            y=1,
            traceorder='normal'
        ),
        margin=dict(l=40, r=40, t=40, b=100),
        height=600,
        width=1000
    )

    #print("Affichage du graphique...")
    fig.show()
    return fig

afficher_linechart_mots()
