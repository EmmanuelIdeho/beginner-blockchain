import json
import hashlib

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_pem_public_key



def generate_keypair():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key

def generate_address(public_key):
    public_bytes = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    return hashlib.sha256(public_bytes).hexdigest()

def create_wallet():
    private_key, public_key = generate_keypair()
    address = generate_address(public_key)
    return private_key, public_key, address

def sign_transaction(private_key, transaction):
    data = json.dumps(transaction, sort_keys=True).encode()
    signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
    return signature.hex()

def verify_transaction(public_key, transaction, signature):
    data = json.dumps(transaction, sort_keys=True).encode()
    coding = bytes.fromhex(signature)
    try:
        public_key.verify(coding, data, ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False

def serialize_public_key(public_key):
    serialized_key = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    return serialized_key.decode('utf-8')

def deserialize_public_key(pem_key):
    deserialized_key = load_pem_public_key(pem_key.encode('utf-8'))
    return deserialized_key


if __name__ == "__main__":
    private_key, public_key, address = create_wallet()
    transaction = {"sender": address, "recipient": "someone", "amount": 10}
    signature = sign_transaction(private_key, transaction)
    pem = serialize_public_key(public_key)
    
    print(f"Address: {address}")
    print(f"Public Key: {pem.replace(chr(10), chr(92) + 'n')}")
    print(f"Signature: {signature}")
