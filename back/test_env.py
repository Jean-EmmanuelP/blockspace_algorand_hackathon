# test_env.py
import os
from dotenv import load_dotenv
import sys

def test_env_reading():
    # Afficher le répertoire courant
    current_dir = os.getcwd()
    print(f"Répertoire courant: {current_dir}")
    
    # Chemin du fichier .env
    env_path = os.path.join(current_dir, '.env')
    print(f"Chemin du fichier .env: {env_path}")
    print(f"Le fichier existe: {os.path.exists(env_path)}")
    
    # Lire et afficher le contenu du fichier .env
    print("\nContenu du fichier .env:")
    try:
        with open(env_path, 'r') as f:
            content = f.read()
            print(content)
            print("\nAnalyse ligne par ligne:")
            for line in content.splitlines():
                print(f"Ligne: '{line}'")
    except Exception as e:
        print(f"Erreur de lecture du fichier: {e}")
    
    # Charger les variables d'environnement
    print("\nChargement des variables avec python-dotenv:")
    load_dotenv(env_path)
    
    # Vérifier les variables
    variables = ['PASSPHRASE', 'ACCOUNT_ADDRESS', 'METADATA_URL', 'METADATA_FILE_PATH']
    for var in variables:
        value = os.getenv(var)
        print(f"{var}: {'DÉFINI' if value else 'NON DÉFINI'}")
        if value:
            print(f"Valeur: {value[:30]}..." if len(str(value)) > 30 else f"Valeur: {value}")
    
    # Vérifier la version de python-dotenv
    print(f"\nVersion de Python: {sys.version}")
    try:
        import dotenv
        print(f"Version de python-dotenv: {dotenv.__version__}")
    except Exception as e:
        print(f"Erreur lors de la vérification de la version de dotenv: {e}")

if __name__ == "__main__":
    test_env_reading()