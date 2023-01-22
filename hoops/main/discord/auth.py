import requests
import os

from dotenv import load_dotenv
load_dotenv()

def exchange_code(code):
    data = {
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET"),
        "grant_type": os.environ.get("GRANT_TYPE"),
        "code": code,
        "redirect_uri": os.environ.get("REDIRECT_URI"),
        "scope": os.environ.get("SCOPE")
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    acess_token = credentials["access_token"]
    # Get user info
    user_response = requests.get("https://discord.com/api/users/@me", headers={
        "Authorization": f"Bearer {acess_token}"
    })
    
    # Get guilds info
    guilds_response = requests.get("https://discord.com/api/users/@me/guilds", headers={
        "Authorization": f"Bearer {acess_token}"
    })
    # Return info
    user = user_response.json()
    guilds = guilds_response.json()
    return [user, guilds]