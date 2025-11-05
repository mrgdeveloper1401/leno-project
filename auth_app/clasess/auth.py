import httpx
from decouple import config


class AuthService:
    def __init__(self):
        self.AUTH_BASE_URL = config('AUTH_BASE_URL', cast=str)
        self.LOGIN_URL = f"{self.AUTH_BASE_URL}/api/v1/user/login/"
        self.VERIFY_URL = f"{self.AUTH_BASE_URL}/api/v1/jwt/create/"
        self.LOGOUT_URL = f"{self.AUTH_BASE_URL}/api/v1/user/logout/"
        self.CIVILREGISTRY = f"{self.AUTH_BASE_URL}/api/v1/kyc/civilregistry/"
        self.REFRESH_TOKEN = f"{self.AUTH_BASE_URL}/api/v1/jwt/refresh/"
        self.API_KEY = config('API_KEY', cast=str)
        self.base_headers = {
            "Content-Type": "application/json",
            "Api-Key": self.API_KEY,
        }

    async def _post(self, url: str, json: dict, headers: dict = None, timeout: int = 20):
        merged_headers = {**self.base_headers}
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=json, headers=merged_headers)
            # response.raise_for_status()
            return response.json()

    async def send_login_request(self, phone: str):
        request_body = {
            "zip_code": "0098",
            "mobile": phone
        }
        return await self._post(self.LOGIN_URL, json=request_body)

    async def verify_code(self, phone: str, code: str):
        request_body = {
            "mobile_number": phone,
            "verify_code": code
        }
        return await self._post(self.VERIFY_URL, json=request_body)

    async def logout(self, access_token: str, refresh_token: str):
        request_body = {
            "refresh_token": refresh_token
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return await self._post(self.LOGOUT_URL, json=request_body, headers=headers)

    async def civil_registry(self, birth_day: str, national_id: str, access_token: str):
        request_body = {
            "national_id": national_id,
            "birth_day": birth_day
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return await self._post(self.CIVILREGISTRY, json=request_body, headers=headers)

    async def rotate_token(self, access_token: str, refresh_token: str):
        request_body = {
            "refresh_token": refresh_token,
        }
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return await self._post(self.REFRESH_TOKEN, json=request_body, headers=headers)
