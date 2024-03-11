import json
import requests
import random
import boto3
from download_clip import download_clip
from datetime import datetime, timedelta

def get_secret(secret_name, region_name="us-east-1"):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
    except Exception as e:
        raise e

def fetch_and_download_twitch_clip(username):
    # Load secrets from the JSON file (In AWS Secrets Manager)
    secrets = get_secret("FirebaseTwitchCredentialsVideoGenerator")


    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": secrets["client_id"],
        "client_secret": secrets["client_secret"],
        "grant_type": "client_credentials",
    }

    response = requests.post(url, params=params)
    data = response.json()
    access_token = data["access_token"]

    headers = {
        "Client-ID": secrets["client_id"],
        "Authorization": f"Bearer {access_token}",
    }

    user_url = f"https://api.twitch.tv/helix/users?login={username}"
    user_response = requests.get(user_url, headers=headers)
    user_data = user_response.json()

    broadcaster_id = user_data["data"][0]["id"]

    now = datetime.utcnow()
    start_date = (now - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    clips_url = f"https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}&started_at={start_date}&ended_at={end_date}"
    clips_response = requests.get(clips_url, headers=headers)
    clips_data = clips_response.json()

    if "data" in clips_data and len(clips_data["data"]) > 0:
        filtered_clips = [clip for clip in clips_data["data"] if clip["duration"] > 15]
        sorted_clips = sorted(
            filtered_clips, key=lambda x: x["view_count"], reverse=True
        )

        random_clip_index = random.randint(0, min(49, len(sorted_clips) - 1))
        most_recent_clip = sorted_clips[random_clip_index]

        thumbnail_url = most_recent_clip["thumbnail_url"]

        download_clip(thumbnail_url)
    else:
        print(f"No clips available for {username}")