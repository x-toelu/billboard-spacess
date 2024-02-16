import requests
from django.conf import settings


class GoogleAuth:
    def __init__(self):
        self.session = requests.Session()

    def get_user_info(self, code):
        access_token = self.__get_access_token(code)
        endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}

        response = self.session.get(
            endpoint,
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        return None

    def __get_access_token(self, code):
        endpoint = 'https://oauth2.googleapis.com/token'

        params = {
            'code': code,
            'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'redirect_uri': "http://localhost:8000/auth/google-redirect/",
            'grant_type': 'authorization_code',
        }

        response = self.session.post(endpoint, data=params)

        if response.status_code == 200:
            return response.json().get('access_token')
        return None
