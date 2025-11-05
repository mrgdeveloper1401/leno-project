import asyncio
import time
from celery import shared_task
from auth_app.clasess import AuthService
from auth_app.models import UserToken


@shared_task(queue="refresh_token", max_retries=3)
def refresh_expiring_tokens():
    now_ts = int(time.time())
    expired_now_ts = now_ts + 30 * 60

    user_tokens = UserToken.objects.filter(expire_in_timestamp__lte=expired_now_ts)

    if not user_tokens:
        return

    auth = AuthService()

    async def process_tokens():
        tasks = []

        async def refresh_single_token(token_obj):
            response = await auth.rotate_token(token_obj.access_token, token_obj.refresh_token)

            if str(response.get("Success")).lower() == "true":
                result = response['Result']
                new_access = result['access_token']
                new_refresh = result['refresh_token']
                new_expire = int(result['user']['expire_in_timestamp'])

                UserToken.objects.filter(user_id=token_obj.user.id).update(
                    access_token=new_access,
                    refresh_token=new_refresh,
                    expire_in_timestamp=new_expire,
                )

        # create list for coroutine
        for i in user_tokens:
            tasks.append(refresh_single_token(i))

        # run task
        await asyncio.gather(*tasks)

    asyncio.run(process_tokens())


@shared_task(queue="logout_user", max_retries=3)
def task_logout_user(access_token: str, refresh_token: str):
    auth = AuthService()

    async def logout_async():
        await auth.logout(access_token, refresh_token)

    asyncio.run(logout_async())


@shared_task(queue="login_user", max_retries=3)
def task_send_login_request(phone: str):

    async def async_request():
        login_service = AuthService()
        result = await login_service.send_login_request(phone)
        return result
    asyncio.run(async_request())
