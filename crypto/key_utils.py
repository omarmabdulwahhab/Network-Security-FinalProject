import os
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

def generate_symmetric_key():
    """Generates a random symmetric key."""
    return get_random_bytes(32)  # 256-bit key

def generate_ecc_key_pair():
    """Generates an ECC key pair for Diffie-Hellman."""
    private_key = ECC.generate(curve='P-256')
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_key(private_key, peer_public_key):
    """Derives a shared key using Diffie-Hellman."""
    shared_secret = private_key.exchange(peer_public_key)
    shared_key = SHA256.new(shared_secret).digest()  # Hash the shared secret
    return shared_key