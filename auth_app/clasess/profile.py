import requests
from decouple import config


class ProfileService:
    def __init__(self):
        self.BASE_URL = config("AUTH_BASE_URL", cast=str)
        self.PROFILE_URL = self.BASE_URL + "/api/v1/user/detail/"
        self.headers = {
            "Content-Type": "application/json",
        }

    def get_profile_details(self, token):
        self.headers["Authorization"] = f"Bearer {token}"
        response = requests.get(self.PROFILE_URL, headers=self.headers)
        return response.json()


# access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYyMTU2OTExLCJpYXQiOjE3NjIxNDk3MTEsImp0aSI6IjI1YzNjZDMyMGY5MzRkNDY4OTQzZGIzNzI0OGRjZDBhIiwidXNlcl9pZCI6IjEwIiwidV9uYW1lIjoiOTM5MTY0MDY2NCIsInRfaWQiOiJlNTBiYzZhZjFkNTVhNmZlZDAxMTZiNGM5NjU4MTkwOTMxNDE3ODgyNTQzOGEzNTgxMmM1MjljMDZhNDQ2YTk2In0.-Q8CxfT-9RQu6xwv-9Flc5aht96WJxlLKh9t50Ofo8g"
# profile = ProfileService()
# profile.get_profile_details(access_token)