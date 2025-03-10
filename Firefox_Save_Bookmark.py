import shutil
import os
import time

def get_firefox_profile_path():
    if os.name == 'nt':  # Windows
        appdata_path = os.environ.get('APPDATA')
        if appdata_path:
            profiles_path = os.path.join(
                appdata_path, 'Mozilla', 'Firefox', 'Profiles')
            if os.path.exists(profiles_path):
                # Rechercher le dossier de profil par défaut
                default_profile = max(
                    [f for f in os.listdir(profiles_path) if os.path.isdir(
                        os.path.join(profiles_path, f))],
                    key=lambda x: len(x)
                )
                return os.path.join(profiles_path, default_profile)
    elif os.name == 'posix':  # macOS ou Linux
        home_path = os.path.expanduser('~')
        profiles_path = os.path.join(home_path, '.mozilla', 'firefox')
        if os.path.exists(profiles_path):
            # Rechercher le dossier de profil par défaut
            default_profile = max(
                [f for f in os.listdir(profiles_path) if os.path.isdir(
                    os.path.join(profiles_path, f))],
                key=lambda x: len(x)
            )
            return os.path.join(profiles_path, default_profile)
    return None

profile_path = get_firefox_profile_path()
print("Chemin du profil : ", profile_path)

if profile_path:
    print("Chemin du profil Firefox par défaut :", profile_path)
else:
    print("Profil Firefox non trouvé.")
    
# Dossier de destination pour les sauvegardes
backup_dir = "D:/Favoris/Save_auto"
print("Chemin du dossier de sauvegarde : ", backup_dir)

copie_effectuee = False  # Variable de contrôle

while not copie_effectuee:
    
    # Récupérer le fichier de sauvegarde le plus récent
    files = os.listdir(profile_path + "/bookmarkbackups")
    latest_file = max(files, key=lambda f: os.path.getmtime(
        profile_path + "/bookmarkbackups/" + f))

    # Copier le fichier de sauvegarde vers le dossier de destination
    shutil.copy2(profile_path + "/bookmarkbackups/" + latest_file, backup_dir)

    # Vérifier si la copie est réussie
    if os.path.exists(backup_dir + "/" + latest_file):
        copie_effectuee = True


print("Fin")
