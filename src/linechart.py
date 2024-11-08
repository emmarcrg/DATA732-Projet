import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from analyse_json_metadata import *

# Les données : on veut le nombre de répétition de chacune des personnes en fonction des mois
analyse_kw_mois('data/fr.sputniknews.africa--20220630--20230630.json', 2023, 2, 'per')
data = {
    "Person": ["Alice", "Bob", "Alice", "Bob", "Alice", "Bob"],
    "Date": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"],
    "Value": [10, 20, 15, 25, 20, 30]
}

df = pd.DataFrame(data)

# Créer une instance Dash
app = dash.Dash(__name__)

# Créer la mise en page de l'application
app.layout = html.Div([
    html.H1("Graphique Linéaire Interactif"),
    dcc.Dropdown(
        id='person-dropdown',
        options=[{'label': person, 'value': person} for person in df['Person'].unique()],
        value=df['Person'].unique()[0]  # Valeur par défaut
    ),
    dcc.Graph(id='line-chart')
])

# Créer le callback pour mettre à jour le graphique en fonction de la sélection du menu déroulant
@app.callback(
    Output('line-chart', 'figure'),
    [Input('person-dropdown', 'value')]
)
def update_chart(selected_person):
    filtered_df = df[df['Person'] == selected_person]
    fig = px.line(filtered_df, x='Date', y='Value', title=f"Évolution de {selected_person}")
    return fig

# Exécuter l'application
if __name__ == '__main__':
    app.run_server(debug=True)
