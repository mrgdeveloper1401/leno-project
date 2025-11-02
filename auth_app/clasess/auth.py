import requests
from decouple import config


class AuthService:
    def __init__(self):
        self.AUTH_BASE_URL = config('AUTH_BASE_URL', cast=str)
        self.LOGIN_URL = self.AUTH_BASE_URL + '/api/v1/user/login/'
        self.VERIFY_URL = self.AUTH_BASE_URL + '/api/v1/jwt/create/'
        self.LOGOUT_URL = self.AUTH_BASE_URL + '/api/v1/user/logout/'
        self.API_KEY = config('API_KEY', cast=str)
        self.headers = {'Content-Type': 'application/json', "Api-Key": self.API_KEY}

    def send_login_request(self, phone):
        """
        Send login request to authentication service
        """
        request_body = {
            "zip_code": "0098",
            "mobile": phone
        }

        response = requests.post(self.LOGIN_URL, json=request_body, headers=self.headers, timeout=20)

        data = response.json()
        return data

    def verify_code(self, phone, code):
        """
        Verify code with authentication service
        """
        request_body = {
            "mobile_number": phone,
            "verify_code": code
        }

        response = requests.post(self.VERIFY_URL, json=request_body, headers=self.headers, timeout=20)

        data = response.json()
        return data

    def logout(self, access_token, refresh_token):
        request_body = {
            "access_token": access_token,
            "Content-Type": "application/json"
        }
        response = requests.post(self.LOGOUT_URL, json=request_body, headers=self.headers, timeout=20)
        print(response)
        return response.json()
