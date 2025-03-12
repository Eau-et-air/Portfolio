
# Lien vers le jeu de données public
## https://www.kaggle.com/datasets/marcelobatalhah/quality-of-life-index-by-country"

# Importer les bibliotèques
import kagglehub  # Facilite l'accès et le téléchargement de jeux de données hébergés sur Kaggle Hub
import os  # Fournit une interface pour interagir avec le système
import pandas as pd  # Pour la manipulation de données
import matplotlib.pyplot as plt  # Pour la création de graphiques
import seaborn as sns  # Plus esthétique que matplotlib

# Récupérer le jeu de données public "Quality of Life Index by Country" (dernière version)
path = kagglehub.dataset_download("marcelobatalhah/quality-of-life-index-by-country")

# Définir le chemin du fichier CSV de l'ensemble de données"
file_path = os.path.join(path, "quality_of_life_indices_by_country.csv")

print("Voici le contenu du fichier",file_path)
print("")


try:
    df = pd.read_csv(file_path)   # Charger les données

    # Obtenir le nombre de colonnes
    nombre_colonnes = df.shape[1]
    print("Le jeux de données contient :",nombre_colonnes, "colonnes")
    print("")
    
    # Renommer les colonnes pour correspondre aux noms de colonnes attendus
    ## Rank, Country, Quality of Life Index, Purchasing Power Index
    ## Safety Index, Health Care Index, Cost of Living Index
    ## Property Price to Income Ratio, Traffic Commute Time Index,
    ## Pollution Index, Climate Index, Year
    df.columns = ["Classement", "Pays", "Qualité de vie","Indice de pouvoir d'achat","Indice de sécurité", "indice des soins de santé", "indice du coût de la vie","Property Price to Income ratio","Indice de temps de trajet","Index Pollution", "Index Climat", "Annee"]

    # Filtrer les données pour l'année 2024
    df_2024 = df[df['Annee'].str.contains('2024')]  # Filtrer sur contient 2024 car il y a des valeurs "2024/2"

    # Sélectionner les 10 premiers pays pour l'année 2024
    top_10_2024 = df_2024.head(10)
    print(top_10_2024)
    print("")
    
    # Création d'un graphique en diagramme à barres
    print("Afficher le diagramme à barres")
    donnees = df['Pays']
    print("==============================")
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Pays', y='Classement', data=top_10_2024, palette='viridis')
    plt.xlabel('Pays')
    plt.ylabel('Classement')
    plt.title('Top 10 des pays par classement (Qualité de vie) - Année 2024')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print(f"Le fichier {file_path} n'a pas été trouvé.")
