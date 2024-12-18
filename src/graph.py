from analyse_json_metadata import *
from analyse_json_data import *
from itertools import combinations, islice
import plotly.graph_objs as go
import networkx as nx
import forceatlas2 as fa2


def normaliser_nom(nom):
    #Permet d'éviter certaines répétition : ne fonctionne certainement que pour quelques valeurs, il y a certainement des oublis dans la liste
    normalisation = {
        'Zelensky': 'Volodymyr Zelensky',
        'Macron': 'Emmanuel Macron',
        'Président russe': 'Vladimir Poutine',  # Ajouter des normalisations pour d'autres doublons connus
        'Poutine': 'Vladimir Poutine',
        'Président ukrainien':'Volodymyr Zelensky',
        'Biden':'Joe Biden'
    }
    return normalisation.get(nom, nom)


# On récupère les n personnes les plus influentes
def pers_importantes(n):
    #On récpère les données : la liste de toutes les personnes citées
    data = analyse_kw('data/fr.sputniknews.africa--20220630--20230630.json', 'per')
    
    # Trier le dictionnaire par ses clés dans l'ordre décroissant
    sorted_data = dict(sorted(data.items(), reverse=True))

    # On fait en sorte qu'il n'y ait pas de répétion/ que les données soient cool :
    # Je sais que c'est pas beau mais au moins c'est fait
    filtered_data = {normaliser_nom(v): k for k, v in sorted_data.items() if 'August' not in v 
                     and 'August 12' not in v and 'Président' not in v 
                     and '© Sputnik' not in v and 'Washington' not in v
                     and 'Wagner' not in v}
    
    #On sélectiuonne les 20 personnes les plus influentes
    data_most = dict(islice(filtered_data.items(), n))
    return data_most

#print(pers_importantes(10))   => retourne les données sous la forme personne : apparition

#On récupère la liste des chaînes de caractères 
def get_noms(n):
    data=pers_importantes(n)
    pers=[]
    
    for personne,cle  in data.items() : 
        pers.append(personne)
    return pers

#print(get_noms()) => retourne le nom des 20 première personnes les plus citées

def initialiser_liens_pers(n):
    personnes_importantes = pers_importantes(n)
    personnes = list(personnes_importantes.keys())
    dictionnaire_liens = {}
    
    for personne1, personne2 in combinations(personnes, 2):
        dictionnaire_liens[(personne1, personne2)] = 0
        dictionnaire_liens[(personne2, personne1)]=0
    
    return dictionnaire_liens

# Exemple d'utilisation :
'''liens = initialiser_liens_pers(20)
print(liens)'''

def initialiser_count(n):
    personnes_importantes = pers_importantes(n)
    count = dict()
    for pers in personnes_importantes:
        count[pers]=0
    return count
        
#On compte le nombre de liens pour chacunes des personnes et on l'ajoute à chaque fois
def get_relations(n):
    data = pd.read_json("data/fr.sputniknews.africa--20220630--20230630.json").get('data')
    pers = get_noms(n)
    links_count = initialiser_liens_pers(n)
    print(links_count)
    apparitions = initialiser_count(n)

    for year in (2022, 2023):
        if year == 2022:
            for month in (7, 8, 9, 10, 11, 12):
                days_in_month = range(1, 32) if month in [7, 8, 10, 12] else range(1, 31)
                for day in days_in_month:
                    articles = recuperer_articles_par_date(data, year, month, day)
                    if articles:
                        people_in_entry = []
                        for article in articles:
                            personnes = recuperer_personnes_par_article(article)
                            if personnes:
                                people_in_entry.extend([person for person in personnes if person in pers])
                        for person1, person2 in combinations(people_in_entry, 2):
                            if person1 != person2:
                                pair = tuple((person1, person2))
                                links_count[pair] += 1
                                pair = tuple((person2, person1))
                                links_count[pair] += 1
                                apparitions[person1]+=1
                                apparitions[person2]+=1
        elif year == 2023:
            for month in (1, 2, 3, 4, 5, 6):
                days_in_month = range(1, 32) if month in [1, 3, 5] else range(1, 30) if month in [4, 6] else range(1, 29)
                for day in days_in_month:
                    articles = recuperer_articles_par_date(data, year, month, day)
                    if articles:
                        people_in_entry = []
                        for article in articles:
                            personnes = recuperer_personnes_par_article(article)
                            if personnes:
                                people_in_entry.extend([person for person in personnes if person in pers])
                        for person1, person2 in combinations(people_in_entry, 2):
                            if person1 != person2:
                                pair = tuple((person1, person2))
                                links_count[pair] += 1
                                pair = tuple((person2, person1))
                                links_count[pair] += 1
                                apparitions[person1]+=1
                                apparitions[person2]+=1
    return links_count, apparitions

#get_relations(10)

#def plot_graph(liens, apparitions, max_node_size, style):
def plot_graph_fa2(liens, apparitions, max_node_size):
    G = nx.Graph()
    
    # Ajouter les arêtes et les poids au graphe
    for (person1, person2), weight in liens.items():
        G.add_edge(person1, person2, weight=weight)
    
    # Utiliser ForceAtlas2 pour la disposition 
    #pos = nx.forceatlas2_layout(G) => ne fonctionne pas
    # pip install fa2_modified ne fonctionne pas non plus : besoin de travailler sur vs et non vscode
        
    #force_atlas_2 : spacialisation
    '''
    Une erreur est présente dans le code de forceatlas2_networkx_layout
    Pour ce faire, il faut modifier le code qui a été importé (avec l'installation sous pip):
    modifié : 
        M = numpy.asarray(networkx.to_numpy_matrix(G)) : to_numpy_matrix n'est plus supporté
    en : 
        M = numpy.asarray(networkx.to_numpy_array(G))

    '''
    pos = fa2.forceatlas2_networkx_layout(G, pos=None, niter=2000)
    
    edge_trace = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2]['weight']
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=weight / 100, color='cornflowerblue'),
            hoverinfo='none',
            mode='lines'))

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    scale_factor = max_node_size / max(apparitions.values())

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        appearances = apparitions.get(node, 0)
        node_text.append(f"{node} ({appearances} apparitions)")
        node_color.append(appearances)
        # Calculer la taille en fonction des apparitions et appliquer la taille maximale
        size = appearances * scale_factor
        node_size.append(size)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=node_text,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            color=node_color,
            size=node_size,
            colorscale='Viridis',
            cmin=0,
            cmax=max(node_color),
            colorbar=dict(
                thickness=15,
                title='Apparitions',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)
        ))
    
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))
    fig.show()

'''links_count, apparitions = get_relations(20)
plot_graph_fa2(links_count, apparitions, 100)'''

def afficher_graph_relations(nb_relations, max_node_size, layout):
    G = nx.Graph()
    liens, apparitions = get_relations(nb_relations)
    
    # Ajouter les arêtes et les poids au graphe
    for (person1, person2), weight in liens.items():
        G.add_edge(person1, person2, weight=weight)
    
    # Sélectionner l'algorithme de disposition
    if layout == 'spring':
        pos = nx.spring_layout(G, k=0.5, iterations=50)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    else:
        raise ValueError("Algorithme de disposition non supporté : {}".format(layout))

    edge_trace = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        weight = edge[2]['weight']
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=weight / 100, color='cornflowerblue'),
            hoverinfo='none',
            mode='lines'))

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    scale_factor = max_node_size / max(apparitions.values())

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        appearances = apparitions.get(node, 0)
        node_text.append(f"{node} ({appearances} apparitions)")
        node_color.append(appearances)
        # Calculer la taille en fonction des apparitions et appliquer la taille maximale
        size = appearances * scale_factor
        node_size.append(size)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=node_text,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            color=node_color,
            size=node_size,
            colorscale='Viridis',
            cmin=0,
            cmax=max(node_color),
            colorbar=dict(
                thickness=15,
                title='Apparitions',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)
        ))
    
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))
    #fig.show()
    return fig


'''links_count, apparitions = get_relations(20)
plot_graph_layout(links_count, apparitions, 100, 'spring')
plot_graph_layout(links_count, apparitions, 100, 'circular') #meilleure spacialisation
plot_graph_layout(links_count, apparitions, 100, 'random')
plot_graph_layout(links_count, apparitions, 100, 'kamada_kawai')'''