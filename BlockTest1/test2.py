from test import Blockchain
import ecdsa

def generate_keys():

    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()

    return public_key.to_string().hex(), private_key.to_string().hex()

sender, sender_private_key = generate_keys()
sender2, sender2_private_key = generate_keys()
receiver, receiver_private_key = generate_keys()
miner, miner_private_key = generate_keys()
amt = 20

# print("sender", sender)
# print("sender_private_key", sender_private_key)
# print("\n")
# print("sender2", sender)
# print("sender2_private_key", sender2_private_key)
# print("\n")
# print("receiver", receiver)
# print("receiver_private_key", receiver_private_key)



blockchain = Blockchain()
blockchain.addTransaction(sender, receiver, amt, sender_private_key)
blockchain.addTransaction(sender2, receiver, amt, sender_private_key)
blockchain.minePendingTransactions(miner)

print(blockchain.getBalance(receiver))
print("\n")
# print(blockchain.displayChain())








