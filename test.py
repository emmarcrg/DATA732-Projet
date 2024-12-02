import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# données à récupérer dans la bdd
matiere="MATH741"
notes_promo=[15, 11, 9, 8, 12, 10, 7, 3, 14, 7, 11, 11, 12, 9]
note_eleve=8

X_notes=list(range(21))
Y_notes=[notes_promo.count(i) for i in X_notes]
couleur=['blue' if i != note_eleve else 'red' for i in X_notes]

moyenne=sum(notes_promo)/len(notes_promo)
ordre_notes=sorted(notes_promo, reverse=True)
classement=ordre_notes.index(note_eleve) + 1

# lancement de Dash
app=dash.Dash(__name__)

app.layout=html.Div([
    html.H1(f"Visualisation des notes", style={'textAlign': 'center'}),
    dcc.Graph(
        id='bar-chart',
        config={'displayModeBar': False}
    ),
    html.Div(
        f"Classement : {classement}e/{len(notes_promo)} - Moyenne : {moyenne:.2f}/20",
        style={'textAlign': 'center', 'fontSize': 18, 'marginTop': 20}
    )
])

@app.callback(
    Output('bar-chart', 'figure'),
    Input('bar-chart', 'id') 
)
def update_chart(_):
    fig=go.Figure()

    fig.add_trace(go.Bar(
        x=X_notes,
        y=Y_notes,
        marker_color=couleur,
        text=[str(y) if y>0 else '' for y in Y_notes],
        textposition='outside',
        name="Nombre d'étudiants"
    ))

    # ajout de la moyenne
    fig.add_vline(
        x=moyenne,
        line=dict(color='green', dash='dash'),
        annotation_text=f"Moyenne : {moyenne:.2f}",
        annotation_position="top right"
    )

    max_y=max(Y_notes)+1 #on ajoute un espace
    fig.update_layout(
        title=f"Distribution des notes en {matiere}",
        xaxis=dict(title='Notes', tickmode='linear', tick0=0, dtick=1),
        yaxis=dict(title="Nombre d'étudiants", range=[0, max_y]),
        showlegend=False,
        plot_bgcolor="rgba(240,240,240,1)"
    )

    return fig

if __name__=='__main__':
    app.run_server(debug=True)
