import os
import json
import hashlib
import base64
from flask import Flask, jsonify, request
from flask_cors import CORS
from algosdk.v2client import algod
from algosdk.transaction import AssetConfigTxn
from datetime import datetime

# Configuration initiale
app = Flask(__name__)
CORS(app)

# Configuration Algorand
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""
MINTED_NFTS_FILE = "minted_nfts.json"

class JSONEncoder(json.JSONEncoder):
    """Encodeur JSON personnalisé pour gérer les types spéciaux"""
    def default(self, obj):
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode('utf-8')
        return super().default(obj)

def serialize_object(obj):
    """Sérialise récursivement un objet en gérant les types spéciaux"""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    elif isinstance(obj, dict):
        return {k: serialize_object(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize_object(item) for item in obj]
    else:
        try:
            # Pour les objets qui ont une méthode de conversion en dict
            return serialize_object(obj.dictify())
        except AttributeError:
            try:
                # Pour les objets qui peuvent être convertis en dict
                return serialize_object(dict(obj))
            except:
                return str(obj)

def get_algod_client():
    """Crée et retourne un client Algorand"""
    return algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "API NFT active",
        "status": "running"
    })

@app.route('/prepare_nft_transaction', methods=['POST'])
def prepare_nft_transaction():
    try:
        # Vérification des paramètres
        request_data = request.get_json()
        if not request_data or 'account_address' not in request_data or 'contract_data' not in request_data:
            return jsonify({"error": "Données manquantes dans la requête"}), 400

        account_address = request_data['account_address']
        contract_data = request_data['contract_data']

        # Vérification du solde
        client = get_algod_client()
        account_info = client.account_info(account_address)
        initial_balance = account_info.get('amount', 0) / 1_000_000
        print(f"Solde du compte: {initial_balance} Algos")

        if initial_balance < 1:
            return jsonify({
                "error": "Solde insuffisant",
                "balance": initial_balance,
                "required": "Au moins 1 Algo",
                "instructions": "Veuillez obtenir des Algos de test sur https://dispenser.testnet.aws.algodev.network/"
            }), 400

        # Préparation des métadonnées
        metadata = {
            "name": contract_data["name"],
            "description": contract_data["description"],
            "image": contract_data["image"],
            "properties": contract_data["properties"]
        }
        metadata_str = json.dumps(metadata)
        
        hash_object = hashlib.new("sha512_256")
        hash_object.update(b"arc0003/amj")
        hash_object.update(metadata_str.encode("utf-8"))
        metadata_hash = hash_object.digest()

        # Obtenir les paramètres de la transaction
        params = client.suggested_params()

        # Créer la transaction non signée
        txn = AssetConfigTxn(
            sender=account_address,
            sp=params,
            total=1,
            default_frozen=False,
            unit_name="NFT",
            asset_name=contract_data["name"],
            manager=account_address,
            reserve=account_address,
            freeze=account_address,
            clawback=account_address,
            url=contract_data["image"],
            metadata_hash=metadata_hash,
            decimals=0
        )

        # Sérialiser la transaction de manière sûre
        response_data = {
            "transaction": serialize_object(txn),
            "metadata": metadata
        }

        return app.json_encoder().encode(response_data), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Erreur lors de la préparation de la transaction NFT: {e}")
        return jsonify({
            "error": str(e),
            "type": str(type(e).__name__)
        }), 500

@app.route('/register_minted_nft', methods=['POST'])
def register_minted_nft():
    try:
        request_data = request.get_json()
        if not all(k in request_data for k in ['account_address', 'contract_data']):
            return jsonify({"error": "Données manquantes"}), 400

        minted_nfts = load_minted_nfts()
        new_nft = {
            "asset_id": 1,
            "title": "testing",
            "description": "description",
            "mint_address": request_data['account_address'],
            "metadata_url": request_data['contract_data']["image"],
            "explorer_url": f"https://testnet.explorer.perawallet.app/asset/{request_data['asset_id']}"
        }
        
        minted_nfts["nfts"].append(new_nft)
        with open(MINTED_NFTS_FILE, 'w') as f:
            json.dump(minted_nfts, f, indent=2)

        return jsonify({"success": True, "nft": new_nft}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def load_minted_nfts():
    try:
        if os.path.exists(MINTED_NFTS_FILE):
            with open(MINTED_NFTS_FILE, 'r') as f:
                return json.load(f)
        return {"nfts": []}
    except Exception as e:
        print(f"Erreur lors du chargement des NFTs mintés: {e}")
        return {"nfts": []}

if __name__ == '__main__':
    print(f"\nDémarrage du serveur Flask...")
    app.json_encoder = JSONEncoder
    app.run(host="0.0.0.0", port=5000, debug=True)