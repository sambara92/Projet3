import os
from os.path import join, isfile
from os import listdir
from datetime import datetime, timedelta
import requests
import pandas as pd

# I. Automatiser le téléchargement des fichiers de données
# Chemin du répertoire d'enregistrement des répertoires
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

# Fonction de téléchargement des fichiers
def download_files():
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

                # Télécharger les fichiers
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

# Def des csv
aeronefs_file = 'aeronefs_2024-06-02.csv'
composants_file = 'composants_2024-06-02.csv'

df_aeronefs = pd.read_csv(aeronefs_file)
df_composants = pd.read_csv(composants_file)

# Charger les nouveaux fichiers de logs de vols et de dégradations
log_path = "data/sauvegarde_log"
listfile_log = [file for file in listdir(log_path) if isfile(join(log_path, file))]

degra_path = "data/sauvegarde_degra"
listfile_degra = [file for file in listdir(degra_path) if isfile(join(degra_path, file))]

# Maj des informations dans df_aeronefs et df_composants
def update_files():
    for log_file in listfile_log:
        df_log = pd.read_csv(join(log_path, log_file))
        for index, row in df_log.iterrows():
            # Exemple de mise à jour pour aeronefs
            if 'aero_linked' in df_log.columns and 'jour_vol' in df_log.columns and 'etat_voyant' in df_log.columns:
                df_aeronefs.loc[df_aeronefs['ref_aero'] == row['aero_linked'], 'last_maint'] = row['jour_vol']
                df_aeronefs.loc[df_aeronefs['ref_aero'] == row['aero_linked'], 'en_maintenance'] = row['etat_voyant']

    for degra_file in listfile_degra:
        df_degra = pd.read_csv(join(degra_path, degra_file))
        for index, row in df_degra.iterrows():
            # Exemple de mise à jour pour composants
            if 'compo_concerned' in df_degra.columns and 'usure_nouvelle' in df_degra.columns:
                df_composants.loc[df_composants['ref_compo'] == row['compo_concerned'], 'taux_usure_actuel'] = row['usure_nouvelle']

    # Sauvegarder des fichiers après maj
    df_aeronefs.to_csv(aeronefs_file, index=False)
    df_composants.to_csv(composants_file, index=False)
    print("Mise à jour des fichiers aeronefs et composants terminée.")

# Exec des fonctions
download_files()
update_files()

download_files()
update_files()
