import hashlib
import datetime

from Health_maker_project.settings import BOT_TOKEN


class httpsServerRequestSecurity:

    SECRET_KEY = BOT_TOKEN

    def __generate_token(self, *args):
        valid_token = []
        minute = datetime.datetime.now().time().minute

        for k in range(minute-3, minute+1):
            data_to_hash = f"{self._data_to_hash_maker(k, *args)}:{self.SECRET_KEY}"
            sha256_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
            valid_token.append(sha256_hash)

        return valid_token

    def _data_to_hash_maker(self, minute, *args):
        data_to_hash = f''

        for i in args:
            if i.isdigit():
                data_to_hash += f"{int(i) * minute}:"
            else:
                data_to_hash += f"{i}:"

        return data_to_hash

    def verify_token(self, token, *args):
        expected_token = self.__generate_token(*args)

        for i in expected_token:
            if token == i:
                return True

        return False
