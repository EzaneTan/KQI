import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class KeyManager:
    """
    RSA key‐pair generator and persister.
    """

    def __init__(self, private_key_path: str, public_key_path: str, passphrase_env: str = "KEY_PASSPHRASE"):
        self.private_path = private_key_path
        self.public_path = public_key_path
        self.passphrase = os.environ.get(passphrase_env, "").encode()

    def generate_rsa_keypair(self, bits: int = 2048):
        """
        Generate and save an RSA keypair.
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537, 
            key_size=bits, 
            backend=default_backend()
        )
        self._save_private_key(private_key)
        self._save_public_key(private_key.public_key())
        return private_key

    def _save_private_key(self, private_key):
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(self.passphrase)
        )
        with open(self.private_path, "wb") as f:
            f.write(pem)

    def _save_public_key(self, public_key):
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(self.public_path, "wb") as f:
            f.write(pem)
