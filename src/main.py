from dash import Dash, html, dcc, callback, Output, Input
import bubble_chart
import linechart

print(f"Module bubble_chart : {bubble_chart}")
print(f"Module linechart : {linechart}")

# Lancement de Dash
app = Dash(__name__)

# Charger les graphiques au démarrage
print("Préchargement des graphiques...")
figure_bubble = bubble_chart.afficher_bubblechart()
print("Bubble chart préchargé")
figure_line = linechart.afficher_linechart()
print("Line chart préchargé")

# Disposition de l'application
app.layout = html.Div([
    html.H1(children='Dashboard', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="chart_selection",
        options=[
            {"label": "Vue globale", "value": "global"},
            {"label": "Bubble Chart", "value": "bubble"},
            {"label": "Line Chart", "value": "line"}
        ],
        value="global"  # La vue globale est la valeur par défaut
    ),
    html.Div(id="graph_container", style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
])

# Mise à jour de l'affichage selon la sélection
@app.callback(
    Output('graph_container', 'children'),
    Input('chart_selection', 'value')
)
def update_graph(chart_type):
    print("Mise à jour de l'affichage")
    
    if chart_type == 'bubble':
        print("Bubble chart sélectionné")
        return dcc.Graph(figure=figure_bubble, style={'width': '100%', 'max-width': '800px', 'height': '400px'})
    elif chart_type == 'line':
        print("Line chart sélectionné")
        return dcc.Graph(figure=figure_line, style={'width': '100%', 'max-width': '800px', 'height': '400px'})
    elif chart_type == 'global':
        print("Vue globale sélectionnée")
        # Liste des graphiques à afficher
        graphs = [
            dcc.Graph(figure=figure_bubble, style={'width': '48%', 'height': '350px', 'margin': '1%'}),
            dcc.Graph(figure=figure_line, style={'width': '48%', 'height': '350px', 'margin': '1%'})
        ]

        num_graphs = len(graphs)
        columns = min(num_graphs, 4)  # Nombre maximum de graphiques par ligne (peut être ajusté)

        # Appliquer les styles calculés à chaque graphique lors de la création
        return html.Div(graphs, style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'})
    
    return html.Div()  # Valeur par défaut si aucune sélection

if __name__ == '__main__':
    print("Lancement de l'application Dash DATA732")
    app.run(debug=True, port=8051)
