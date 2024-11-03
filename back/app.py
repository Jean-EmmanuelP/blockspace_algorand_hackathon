import os
import json
import hashlib
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, url_for, flash
from algokit_utils.beta.algorand_client import AlgorandClient, AssetCreateParams
import algokit_utils
from algosdk import account, mnemonic
import certifi

# Charger le certificat SSL pour les connexions Algonode
os.environ['SSL_CERT_FILE'] = certifi.where()

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Nécessaire pour utiliser flash

# Récupérer les variables d'environnement
PASSPHRASE = os.getenv("PASSPHRASE")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
METADATA_URL = os.getenv("METADATA_URL")
METADATA_FILE_PATH = os.getenv("METADATA_FILE_PATH")

class AlgorandActions:
    def __init__(self):
        self.algorand_client = self.connect_to_algorand_testnet()

    def connect_to_algorand_testnet(self):
        # Connexion au TestNet d'Algorand
        return AlgorandClient.test_net()

    def get_account_from_passphrase(self, passphrase):
        # Récupérer les informations du compte depuis le passphrase
        return algokit_utils.get_account_from_mnemonic(passphrase)

    def load_metadata_from_file(self, file_path):
        # Charger le fichier JSON de métadonnées
        with open(file_path, "r") as f:
            metadata_json = json.load(f)
        return json.dumps(metadata_json)

    def create_metadata_hash(self, metadata_str):
        # Créer le hash des métadonnées
        hash_object = hashlib.new("sha512_256")
        hash_object.update(b"arc0003/amj")
        hash_object.update(metadata_str.encode("utf-8"))
        return hash_object.digest()

    def create_asa(self, creator_address, total):
        # Logique pour créer un ASA
        account_info = self.get_account_from_passphrase(PASSPHRASE)
        if creator_address != account_info.address:
            raise ValueError("L'adresse du créateur ne correspond pas à l'adresse du compte.")

        metadata_str = self.load_metadata_from_file(METADATA_FILE_PATH)
        metadata_hash = self.create_metadata_hash(metadata_str)

        sent_txn = self.algorand_client.send.asset_create(
            AssetCreateParams(
                sender=account_info.address,
                signer=account_info.signer,
                total=total,
                asset_name="NFTAsset",
                unit_name="NFT",
                manager=account_info.address,
                clawback=account_info.address,
                freeze=account_info.address,
                url=METADATA_URL,
                metadata_hash=metadata_hash,
                decimals=0
            )
        )
        asset_id = sent_txn["confirmation"]["asset-index"]
        tx_id = sent_txn["transaction"]["id"]
        return asset_id, tx_id

# Initialize AlgorandActions
algo = AlgorandActions()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Bienvenue à l'API NFT. Utilisez /create_nft pour créer un NFT."})

@app.route('/create_asa', methods=['POST'])
def create_asa():
    """
    Creates a new Algorand Standard Asset (ASA) and logs the creation in the blockchain activity log.
    """
    creator_address = request.form.get('creator_address')
    total = int(request.form.get('total'))
    
    try:
        asset_id, tx_id = algo.create_asa(creator_address, total)
        # Assuming blockchain_activity is a list to log activities
        blockchain_activity.append((tx_id, creator_address, 'ASA Created', asset_id))
        flash(f"Created ASA with Asset ID: {asset_id} and a total of {total}", 'success')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"Error creating ASA: {str(e)}", 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
