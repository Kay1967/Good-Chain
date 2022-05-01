from tkinter.messagebox import NO
from cryptography.exceptions import *
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import pickle

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt(message, key):
    
    try:
        ciphertext = key.encrypt(message,
                                padding.OAEP(
                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                    algorithm=hashes.SHA256(),
                                    label=None))
        return ciphertext
    except:
        return False

def decrypt(ciphertext, key):
    try:
        plaintext = key.decrypt(
                                ciphertext,
                                padding.OAEP(
                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                    algorithm=hashes.SHA256(),
                                    label=None))
        return plaintext
    except:
        return False

def save_keys(keys_file_name, keys_list):
    keys_ser_list = []
    for item in keys_list:
        key_name, private_key, public_key = item
    
        prv_ser = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()  
                    )
        pbc_ser = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
        
        keys_ser_list.append((key_name, prv_ser, pbc_ser))
    
    savefile = open(keys_file_name, "wb")
    pickle.dump(keys_ser_list, savefile)
    savefile.close()

def load_keys(keys_file_name):
    loadfile = open(keys_file_name, "rb")
    keys_list_ser = pickle.load(loadfile)
    loadfile.close()

    keys_list = []
    for item in keys_list_ser:
        key_name, private_key_ser, public_key_ser = item
        private_key = serialization.load_pem_private_key(private_key_ser,password=None)
        public_key = serialization.load_pem_public_key(public_key_ser)

        keys_list.append((key_name, private_key, public_key))
    return keys_list

def signature(message, private_key):
  signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

def verification(msg, signature, key):
  try:
    return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-1'
  except:
    return False


