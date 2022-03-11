import json
import sys
from itertools import cycle

import app_logger
from error_messages import ErrorMessages

logger = app_logger.get_logger(__name__)


class PhasmoSaveDataDecoder:
    def __init__(
        self,
        encrypted_file_name="saveData.txt",
    ):
        self.encrypted_file_name = encrypted_file_name
        self.decrypted_file_name = f"decrypted_{self.encrypted_file_name}"
        self.key = self._load_key()
        logger.debug(f"Object PhasmoSaveDataDecoder created: {self}")

    def _get_masked_key(self):
        return self.key[:2] + "*" * 9 + self.key[-2:]

    def _load_key(self):
        try:
            with open("key.txt") as key_file:
                self.key = "".join(key_file.readlines())
                logger.debug(f"Key from key.txt is loaded {self._get_masked_key()}")
                return self.key
        except EnvironmentError:
            logger.debug(ErrorMessages.KEY_FILE_PROBLEM.value)
            sys.exit(1)

    def _crypt(self, data):
        xored = "".join(chr(ord(x) ^ ord(y)) for (x, y) in zip(data, cycle(self.key)))

        return xored

    def encrypt(self):
        try:
            with open(self.decrypted_file_name, "r") as decrypted_file, open(
                self.encrypted_file_name, "w"
            ) as encrypted_file:
                data = decrypted_file.read()
                encrypted_data = self._crypt(data=data)

                encrypted_file.write(encrypted_data)
                logger.debug(f"Encrypted file created: {self.encrypted_file_name}")
        except EnvironmentError:
            logger.debug(ErrorMessages.DECRYPTED_FILE_PROBLEM.value)
            sys.exit(1)

        return self

    def decrypt(self):
        try:
            with open(self.encrypted_file_name, "r") as encrypted_file, open(
                self.decrypted_file_name, "w"
            ) as decrypted_file:
                data = encrypted_file.read()
                decrypted_data = self._crypt(data=data)

                decrypted_file.write(decrypted_data)
                logger.debug(f"Decrypted file created: {self.decrypted_file_name}")
        except EnvironmentError:
            logger.debug(ErrorMessages.ENCRYPTED_FILE_PROBLEM.value)
            sys.exit(1)

        return self

    def set_money(self, amount=9999999):
        try:
            with open(self.decrypted_file_name, "r+") as f:
                data = f.read()
                json_data = json.loads(data)

                for i in range(len(json_data.get("IntData", []))):
                    if json_data.get("IntData", [])[i].get("Key", {}) == "PlayersMoney":
                        json_data.get("IntData", [])[i]["Value"] = str(amount)
                        logger.debug(f"Amount of money is set to {amount}")

                f.seek(0)
                f.truncate()
                f.writelines(json.dumps(json_data))
        except EnvironmentError:
            logger.debug(ErrorMessages.DECRYPTED_FILE_PROBLEM.value)
            sys.exit(1)

        except json.decoder.JSONDecodeError:
            logger.debug(ErrorMessages.JSON_CORRUPTED.value)
            sys.exit(1)

        return self

    def __repr__(self):
        return f"{self.encrypted_file_name=} {self.decrypted_file_name=} self.key={self._get_masked_key()}"
