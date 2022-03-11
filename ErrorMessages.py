from enum import Enum


class ErrorMessages(Enum):
    ENCRYPTED_FILE_PROBLEM = (
        "Problem with encrypted file. Place it in folder with this script."
    )
    DECRYPTED_FILE_PROBLEM = (
        "Problem with decrypted file. Please decrypt your saveData.txt file first."
    )
    KEY_FILE_PROBLEM = (
        "Problem with key file. Please place your key.txt in folder with this script"
    )
