from itertools import cycle
import json


class PhasmoSaveDataDecoder:
    def __init__(
        self,
        encrypted_file_name="saveData.txt",
        key="CHANGE ME TO YOUR OWN RANDOM STRING",
    ):

        self.encrypted_file_name = encrypted_file_name
        self.decrypted_file_name = f"decrypted_{self.encrypted_file_name}"
        self.key = key

    def _crypt(self, data):
        xored = "".join(chr(ord(x) ^ ord(y)) for (x, y) in zip(data, cycle(self.key)))

        return xored

    def encrypt(self):
        with open(self.decrypted_file_name, "r") as decrypted_file, open(
            self.encrypted_file_name, "w"
        ) as encrypted_file:
            data = decrypted_file.read()
            encrypted_data = self._crypt(data=data)

            encrypted_file.write(encrypted_data)
            print(f"Check encrypted data in {self.encrypted_file_name}")

        return self

    def decrypt(self):
        with open(self.encrypted_file_name, "r") as encrypted_file, open(
            self.decrypted_file_name, "w"
        ) as decrypted_file:
            data = encrypted_file.read()
            decrypted_data = self._crypt(data=data)

            decrypted_file.write(decrypted_data)
            print(f"Check decrypted data in {self.decrypted_file_name}")

        return self

    def set_money(self, amount=9999999):
        with open(self.decrypted_file_name, "r+") as f:
            data = f.read()
            json_data = json.loads(data)

            for i in range(len(json_data.get("IntData", []))):
                if json_data.get("IntData", [])[i].get("Key", {}) == "PlayersMoney":
                    json_data.get("IntData", [])[i]["Value"] = str(amount)
                    print(f"Amount of money is set to {amount}")

            f.seek(0)
            f.truncate()
            f.writelines(json.dumps(json_data))

        return self



