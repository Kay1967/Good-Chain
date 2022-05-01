from cryptography.exceptions import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def generate_keys():
  private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
  public_key = private_key.public_key()
  
  return private_key, public_key

def sign(message, private_key):
    signature = private_key.sign(
    bytes(str(message), 'UTF-8'),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256())
    return signature

def verify(message, signature, public_key):
    try:
        output = public_key.verify(
            signature,
            bytes(str(message), 'UTF-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256())
        return True
    except:
        return False