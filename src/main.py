from dash import Dash, html, dcc, callback, Output, Input
import bubble_chart
import linechart_personnes
import linechart_mots

print(f"Module bubble_chart : {bubble_chart}")
print(f"Module linechart des personnes : {linechart_personnes}")
print(f"Module linechart des mots-clés : {linechart_mots}")

# Lancement de Dash
app = Dash(__name__)

# Charger les graphiques au démarrage
print("Préchargement des graphiques...")
figure_bubble = bubble_chart.afficher_bubblechart()
print("Bubble chart préchargé")
figure_line_personnes = linechart_personnes.afficher_linechart_personnes()
print("Line chart des personnes préchargé")
figure_line_mots = linechart_mots.afficher_linechart_mots()
print("Line chart des mots-clés préchargé")

# Disposition de l'application
app.layout = html.Div([
    html.H1(children='Dashboard', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="chart_selection",
        options=[
            {"label": "Vue globale", "value": "global"},
            {"label": "Bubble Chart", "value": "bubble"},
            {"label": "Line Chart des personnes", "value": "line_personnes"},
            {"label": "Line Chart des mots-clés", "value": "line_mots"},
        ],
        value="global"
    ),
    html.Div(id="graph_container")
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
        return dcc.Graph(figure=figure_bubble)
    elif chart_type == 'line_personnes':
        print("Line chart des personnes sélectionné")
        return dcc.Graph(figure=figure_line_personnes)
    elif chart_type == "line_mots":
        print("Line chart des mots-clés sélectionné")
        return dcc.Graph(figure=figure_line_mots)
    elif chart_type == 'global':
        print("Vue globale sélectionnée")
        # Liste des graphiques à afficher pour la vue globale
        graphs = [
            html.Div(dcc.Graph(figure=figure_bubble), style={'margin-bottom': '20px'}),
            html.Div(dcc.Graph(figure=figure_line_personnes), style={'margin-bottom': '20px'}),
            html.Div(dcc.Graph(figure=figure_line_mots))
        ]

        # Retourne la liste de graphiques pour la vue globale
        return html.Div(graphs, style={'display': 'block'})
    
    return html.Div()  # Valeur par défaut si aucune sélection

if __name__ == '__main__':
    print("Lancement de l'application Dash DATA732")
    app.run(debug=True, port=8051)