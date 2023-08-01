import datetime

from __health_maker_bot.https_request_security import httpsRequestSecurity
from __health_maker_bot.https_requests import HttpsRequestsServer


class LocationProcessing:
    def __init__(self):
        self.security_https = httpsRequestSecurity()
        self.server_request = HttpsRequestsServer()

    async def get_coordinates(self, message):
        longitude = message.location.longitude
        latitude = message.location.latitude

        return [latitude, longitude]

    async def request_coordinates(self, message, url):
        telegram_id = str(message.from_user.id)
        coordinates = await self.get_coordinates(message)
        coordinates = str(coordinates).replace(', ', '!&').replace('[', '').replace(']', '')

        token = self.security_https.generate_token(telegram_id, coordinates)
        result = await self.server_request.post_running_training_data(url,
                                                                      token,
                                                                      telegram_id,
                                                                      coordinates)

        return result

    async def requests_finish_location(self, callback, url):
        telegram_id = str(callback.message.chat.id)
        user_ft = str(datetime.datetime.now())

        token = self.security_https.generate_token(telegram_id, user_ft)
        result = await self.server_request.post_running_finish_training_data(url,
                                                                             token,
                                                                             telegram_id,
                                                                             user_ft)

        return result

