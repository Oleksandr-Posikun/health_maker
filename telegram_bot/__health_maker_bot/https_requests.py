import datetime
import aiohttp


class HttpsRequestsServer:
    def __init__(self):
        self.url_server = 'http://127.0.0.1:8000'

    async def _get_request(self, *args, json: bool = True, text: bool = True,):
        async with aiohttp.ClientSession() as session:
            url = f'{self.url_server}'

            for i in args:
                url += f'/{str(i)}'

            async with session.get(url, timeout=3) as response:
                if json:
                    return await response.json()
                elif text:
                    return await response.text()
                else:
                    return response

    async def _post_request(self, *args, json: bool = False, text: bool = False, **kwargs):
        async with aiohttp.ClientSession() as session:
            url = f'{self.url_server}'
            headers = {}

            for i in args:
                url += f'/{str(i)}'

            for key, value in kwargs.items():
                key = key.replace('_', '-')
                headers[key] = value

            async with session.post(url, headers=headers) as response:
                if json:
                    return await response.json()

                if text:
                    return await response.text()

                return response

    async def post_user_info(self, url, token, telegram_id, user_name):
        response = await self._post_request(url,  User_Agent='TelegramBot',
                                            Authorization=token,
                                            user=telegram_id,
                                            user_name=user_name,
                                            json=True)

        return response

    async def post_running_training_data(self, url, token, telegram_id, coordinates):
        response = await self._post_request(url, User_Agent='TelegramBot',
                                            Authorization=token,
                                            user=telegram_id,
                                            user_position=coordinates,
                                            )

        return response.status

    async def post_running_finish_training_data(self, url, token, telegram_id, finish_time):
        response = await self._post_request(url,
                                            User_Agent='TelegramBot',
                                            Authorization=token,
                                            user=telegram_id,
                                            finish_time=finish_time,
                                            json=True)

        return response

