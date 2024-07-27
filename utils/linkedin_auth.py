import requests
from config.settings import LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET, LINKEDIN_REDIRECT_URI

class LinkedInAuth:
    def __init__(self):
        self.client_id = LINKEDIN_CLIENT_ID
        self.client_secret = LINKEDIN_CLIENT_SECRET
        self.redirect_uri = LINKEDIN_REDIRECT_URI
        self.scope = 'w_member_social'
        self.auth_url = f'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={self.scope}'
        self.token_url = 'https://www.linkedin.com/oauth/v2/accessToken'

    def get_authorization_url(self):
        return self.auth_url

    def get_access_token(self, auth_code):
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to get access token: {response.text}")

    def refresh_access_token(self, refresh_token):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to refresh access token: {response.text}")