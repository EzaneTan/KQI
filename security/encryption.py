from cryptography.fernet import Fernet

class EncryptionService:
    """
    Symmetric encryption/decryption service using Fernet.
    """

    def __init__(self, key: bytes):
        self.fernet = Fernet(key)

    @staticmethod
    def generate_key() -> bytes:
        """
        Generate a fresh 32-byte Fernet key.
        """
        return Fernet.generate_key()

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt a byte payload.
        """
        return self.fernet.encrypt(data)

    def decrypt(self, token: bytes) -> bytes:
        """
        Decrypt a ciphertext.
        """
        return self.fernet.decrypt(token)
