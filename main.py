from flask import Flask, request, jsonify
import swiftclient
import hmac
import hashlib
import time
from urllib.parse import quote

app = Flask(__name__)

# Configuration OVH
AUTH_URL = 'https://auth.cloud.ovh.net/v3'
REGION_NAME = 'GRA'
USER = 'user-RAqDwcWqKbhS'
KEY = 'k2EsKaGyy3BC3xDRrVmXhsspNCrw74uN'
PROJECT_ID = '2b45951fb19c42d197be8ee756932ff1'
USER_ID = 'ccabed683df844d9aebb49b9a7eaaba7'

# Container et clé temporaire
CONTAINER_NAME = 'muslim.vibes'
TEMP_URL_KEY = 'Harris91270.'  # C'est à toi de la définir et de la mettre sur ton container

def get_ovh_connection():
    return swiftclient.Connection(
        user=USER,
        key=KEY,
        authurl=AUTH_URL,
        os_options={
            'project_id': PROJECT_ID,
            'user_id': USER_ID,
            'region_name': REGION_NAME
        },
        auth_version='3'
    )

def generate_temp_url(container, object_name, key, method='GET', expires_in=3600):
    conn = get_ovh_connection()
    storage_url = conn.get_auth()[0]

    expires = int(time.time() + expires_in)
    path = f'/v1/AUTH_{PROJECT_ID}/{container}/{quote(object_name)}'
    hmac_body = f'{method}\n{expires}\n{path}'
    sig = hmac.new(
        key.encode('utf-8'),
        hmac_body.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()

    temp_url = f'{storage_url}{path}?temp_url_sig={sig}&temp_url_expires={expires}'
    return temp_url

@app.route('/generate-url', methods=['GET'])
def generate_url():
    video_key = request.args.get('video')
    if not video_key:
        return jsonify({'error': 'Missing "video" parameter'}), 400
    try:
        url = generate_temp_url(CONTAINER_NAME, video_key, TEMP_URL_KEY)
        return jsonify({'url': url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
