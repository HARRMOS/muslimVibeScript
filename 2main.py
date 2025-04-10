from flask import Flask, jsonify, request
import boto3
import datetime
from botocore.signers import CloudFrontSigner

app = Flask(__name__)

# Remplace par tes clés OVH
aws_access_key = "435971df068347ee833dedcb0e35ed3b"
aws_secret_key = "687d0d8a3b9f40d18d2fcacca7216ae9"

# Connexion au S3 OVH
s3_client = boto3.client(
    's3',
    endpoint_url='https://s3.eu-west-par.io.cloud.ovh.net',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

@app.route('/generate-url', methods=['GET'])
def generate_url():
    # Récupérer le paramètre 'video' depuis l'URL
    video_key = request.args.get('video')
    
    if not video_key:
        return jsonify({"error": "Missing 'video' parameter"}), 400
    
    # Générer l'URL pré-signée pour le fichier spécifié
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'muslim.vibes', 'Key': video_key},
            ExpiresIn=3600  # Durée de validité (en secondes)
        )
        return jsonify({'url': url})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
