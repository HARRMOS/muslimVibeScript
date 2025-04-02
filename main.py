from flask import Flask
import boto3
import datetime

app = Flask(__name__)

@app.route('/')
def generate_presigned_url():
    aws_access_key = "435971df068347ee833dedcb0e35ed3b"
    aws_secret_key = "687d0d8a3b9f40d18d2fcacca7216ae9"

    s3_client = boto3.client(
        's3',
        endpoint_url='https://s3.eu-west-par.io.cloud.ovh.net',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'muslim.vibes', 'Key': 'message.mp4'},
        ExpiresIn=3600
    )

    return url

if __name__ == "__main__":
    port = 5000  # Railway fournit un port dynamique, donc tu peux utiliser le port donné dans l'environnement
    app.run(host="0.0.0.0", port=port)
