import boto3
import datetime
from botocore.signers import CloudFrontSigner

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

# Génération de l'URL pré-signée
url = s3_client.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'muslim.vibes', 'Key': 'message.mp4'},
    ExpiresIn=3600  # Durée de validité (en secondes)
)

print(url)
