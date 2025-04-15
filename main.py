import swiftclient
import hashlib
import hmac
import time
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ------------------ Connexion à OVH ------------------
def get_ovh_connection():
    return swiftclient.Connection(
        user='user-RAqDwcWqKbhS',
        key='k2EsKaGyy3BC3xDRrVmXhsspNCrw74uN',
        authurl='https://auth.cloud.ovh.net/v3',
        os_options={
            'project_id': '2b45951fb19c42d197be8ee756932ff1',
            'user_id': 'ccabed683df844d9aebb49b9a7eaaba7',
            'region_name': 'GRA'
        },
        auth_version='3'
    )

# ------------------ Clé secrète TempURL ------------------
TEMP_URL_KEY = 'Harris91270.'  # Tu peux choisir ce que tu veux
CONTAINER_NAME = "Muslim.Vibes/Contents"

# ------------------ Route pour générer une URL temporaire ------------------

@app.route("/get_temp_url", methods=["GET"])
def generate_temp_url():
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Paramètre 'filename' manquant."}), 400

    method = "GET"
    expires_in = 3600
    expires = int(time.time() + expires_in)

    path = f"/v1/AUTH_2b45951fb19c42d197be8ee756932ff1/{CONTAINER_NAME}/{filename}"
    sig = hmac.new(
        key=TEMP_URL_KEY.encode(),
        msg=f"{method}\n{expires}\n{path}".encode(),
        digestmod=hashlib.sha1
    ).hexdigest()

    public_url = f"https://storage.gra.cloud.ovh.net{path}"
    temp_url = f"{public_url}?temp_url_sig={sig}&temp_url_expires={expires}"

    return jsonify({"temp_url": temp_url})

# ------------------ Route pour définir la clé TempURL une fois ------------------
@app.route("/set_temp_url_key", methods=["POST"])
def set_temp_key():
    try:
        conn = get_ovh_connection()
        conn.post_container(CONTAINER_NAME, headers={
            'X-Container-Meta-Temp-URL-Key': TEMP_URL_KEY
        })
        return jsonify({"message": "Clé TempURL définie avec succès."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------ Run ------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
