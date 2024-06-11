import os
from os import listdir, join
from datetime import datetime
import requests
import pandas as pd

# I. Automatiser le téléchargement des fichiers de données
# But : Créer un script qui télécharge les fichiers au fil des jours et 
#       évite de télécharger à nouveau les fichiers déjà téléchargés
#       (Fichiers publiés chaque jour)
# Inconvénient : nécessite de créer un script de job en local pour faire tourner chaque jour  
#               Si un fichier n'est pas récupéré le jour même, il ne peut pas être récupéré le jour suivant

# Chemin du répertoire d'enregistrement des répertoires (identique au notebook)
working_directory = os.getcwd()
print(f"Chemin d'accès au répertoire : {working_directory}")

# Création des dossiers pour stocker les fichiers téléchargés
os.makedirs("data/sauvegarde_log", exist_ok=True)
os.makedirs("data/sauvegarde_degra", exist_ok=True)

# Créer une fonction pour obtenir la date du jour
def get_today():
    today = datetime.today()
    return today.strftime("%Y-%m-%d")

# Récupérer année/mois/jour actuel
current_year = datetime.now().year
current_month = datetime.now().month
current_day = datetime.now().day

# Utiliser la fonction today
today = get_today()

# Construction de l'url de téléchargement en fonction du mois et du jour
for year in range(current_year, current_year + 1):
    for month in range(current_month, current_month + 1):
        for day in range(current_day, current_day + 1):
            if year == current_year and month == current_month and day > current_day:  # Ignorer les fichiers supérieurs à la date d'aujourd'hui
                continue
            if f"{year}-{month:02d}-{day:02d}" < today:  # Ignorer les fichiers déjà téléchargés
                continue

            url_log_vol = f"http://sc-e.fr/docs/logs_vols_{year}-{month:02d}-{day:02d}.csv"
            file_log = f"data/sauvegarde_log/logs_vols_{year}-{month:02d}-{day:02d}.csv"

            url_degrad = f"http://sc-e.fr/docs/degradations_{year}-{month:02d}-{day:02d}.csv"
            file_degrad = f"data/sauvegarde_degra/degradations_{year}-{month:02d}-{day:02d}.csv"

            # Télécharger le fichier
            print(f"Téléchargement de {file_log}")
            response_log = requests.get(url_log_vol)
            print(f"Téléchargement de {file_degrad}")
            response_degrad = requests.get(url_degrad)

            # Si réponse 200, on réalise le téléchargement
            if response_log.status_code == 200:
                with open(file_log, "wb") as file_log_vol:
                    file_log_vol.write(response_log.content)
            else:
                print(f"Téléchargement impossible de {file_log}. Code statut {response_log.status_code}")

            if response_degrad.status_code == 200:
                with open(file_degrad, "wb") as file_degradation:
                    file_degradation.write(response_degrad.content)
            else:
                print(f"Téléchargement impossible de {file_degrad}. Code statut {response_degrad.status_code}")

print("Téléchargement terminé")

# Vérifier le nombre de fichiers téléchargés dans sauvegarde_log
log_path = "data/sauvegarde_log"
listfile_log = [file for file in listdir(log_path) if isfile(join(log_path, file))]
print(f"Nb fichier log_vol: {len(listfile_log)}")

degra_path = "data/sauvegarde_degra"
listfile_degra = [file for file in listdir(degra_path) if isfile(join(degra_path, file))]
print(f"Nb fichier degradation: {len(listfile_degra)}")

# Vérifier l'ouverture d'un fichier log_vol
link_log = 'data/sauvegarde_log/logs_vols_2024-06-05.csv'
df_log = pd.read_csv(link_log)
print(df_log.head())

# Vérifier l'ouverture d'un fichier degradation
link_degra = 'data/sauvegarde_degra/degradations_2024-06-05.csv'
df_degra = pd.read_csv(link_degra)
print(df_degra.head())