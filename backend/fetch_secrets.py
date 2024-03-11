import boto3
import json

def get_secret(secret_name, region_name='us-west-2'):
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret = response['SecretString']
        return json.loads(secret)
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise e

# Usage example
if __name__ == "__main__":
    secret_name = 'MyApp_Firebase_Twitch_Credentials'
    secrets = get_secret(secret_name)
    print(secrets)
