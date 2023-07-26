import hashlib
import os
import datetime


class httpsRequestSecurity:

    SECRET_KEY = str(os.getenv("BOT_TOKEN"))

    def generate_token(self, *args):
        data_to_hash = f"{self._data_to_hash_maker(*args)}:{self.SECRET_KEY}"
        sha256_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()

        return sha256_hash

    def _data_to_hash_maker(self, *args):
        minute = datetime.datetime.now().time().minute

        data_to_hash = f''

        for i in args:
            if i.isdigit():
                data_to_hash += f"{int(i) * minute}:"
            else:
                data_to_hash += f"{i}:"

        return data_to_hash
