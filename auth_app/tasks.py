import time
from celery import shared_task
from auth_app.clasess import AuthService
from auth_app.models import UserToken


@shared_task
def refresh_expiring_tokens():
    now_ts = int(time.time())
    expired_now_ts = now_ts + 30 * 60

    user_token = UserToken.objects.filter(
        expire_in_timestamp__lte=expired_now_ts
    )

    # auth
    auth = AuthService()

    for i in user_token:
        try:
            # send request into api
            response = auth.rotate_token(i.access_token, i.refresh_token)

            # check response
            if str(response.get("Success")).lower() == "true":

                # get information on response
                access_token = response['Result']['access_token']
                refresh_token = response['Result']['refresh_token']
                expire_in_timestamp = int(response['Result']['user']['expire_in_timestamp'])

                # update information
                UserToken.objects.filter(
                    user_id=i.user.id
                ).update(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    expire_in_timestamp=expire_in_timestamp,
                )
        except Exception as e:
            print(f"Failed to refresh token for user {i.user.id}: {e}")
            continue
