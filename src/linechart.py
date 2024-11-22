import matplotlib.pyplot as plt
import pandas as pd
from analyse_json_metadata import *

def normaliser_nom(nom):
    normalisation = {
        'Zelensky': 'Volodymyr Zelensky',
        'Macron': 'Emmanuel Macron',
        'Président russe': 'Vladimir Poutine',  # Ajouter des normalisations pour d'autres doublons connus
        'Poutine': 'Vladimir Poutine'
    }
    return normalisation.get(nom, nom)

# Créer un dictionnaire pour stocker les données par mois
data_by_month = {}
for annee, mois in [(2022, m) for m in range(8, 13)] + [(2023, m) for m in range(1, 7)]:  # Ajouter les mois de 2023 jusqu'à juin
    raw_data = analyse_kw_mois('data/fr.sputniknews.africa--20220630--20230630.json', annee, mois, 'per')
    
    # Filtrer les clés 
    # Je sais que c'est pas beau mais au moins c'est fait
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

# Vérifier que les données sont bien numériques
print(df.dtypes)

# Convertir toutes les colonnes en type numérique (si nécessaire)
df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

# Créer le diagramme en barres empilées
ax = df.plot(kind='bar', stacked=True, figsize=(10, 5))

print(df.head())

# Ajouter les titres et les labels
plt.title('Diagramme en barres empilées des Personnes par Mois')
plt.xlabel('Mois')
plt.xticks(rotation=90)
plt.ylabel('Valeurs')

# Afficher la légende et ajuster la mise en page
plt.legend(title='Personnes', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
