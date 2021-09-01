from ecdsa import SigningKey
import ecdsa
from hashlib import sha256


private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
msg = bytes("Educative authorizes this shot", 'utf-8')
signature = private_key.sign(msg)
#print(signature)    
public_key = private_key.get_verifying_key()
print(public_key)
print("Verified:", public_key.verify(signature, msg), "\n")


print("Private Key as Object",private_key)
sk = private_key.to_string().hex()
print("Private Key as hex",sk)
sk = ecdsa.SigningKey.from_string(bytes.fromhex(sk), curve=ecdsa.SECP256k1) 
print("Private Key as Object",sk)

print("\n")

print("Public Key as Object",public_key)
vk = public_key.to_string().hex()
print("Public Key as hex",vk)
vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(vk), curve=ecdsa.SECP256k1) 
print("Public Key as Object",vk)
