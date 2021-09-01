import json
import ecdsa
from datetime import datetime
from blake3 import blake3
from hashlib import sha256


class Blockchain ():
	def __init__(self):
		self.chain = [self.addGenesisBlock()]
		self.pendingTransactions = []
		self.difficulty = 2
		self.minerRewards = 50
		self.blockSize = 10
		self.nodes = set()

	# def register_node(self, address):
	# 	parsedUrl = urlparse(address)
	# 	self.nodes.add(parsedUrl.netloc)

	def displayChain(self):
		return self.chain


	def minePendingTransactions(self, miner):
		
		lenPT = len(self.pendingTransactions)
		if(lenPT <= 1):
			print("Not enough transactions to mine! (Must be > 1)")
			return False
		else:
			for i in range(0, lenPT, self.blockSize):

				end = i + self.blockSize
				if i >= lenPT:
					end = lenPT
				
				transactionSlice = self.pendingTransactions[i:end]

				newBlock = Block(transactionSlice, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), len(self.chain))
				

				hashVal = self.getLastBlock().hash
				newBlock.prev = hashVal
				newBlock.mineBlock(self.difficulty)
				if self.isValidChain():
					self.chain.append(newBlock)
					print("Mining Transactions Success!")
					payMiner = Transaction("Miner Rewards", miner, self.minerRewards)
					self.pendingTransactions = [payMiner]
				else:
					return False

		return True

	def addTransaction(self, sender, receiver, amt, senderKey):
		#DECODE SENDER RECEIVER KEY IN test FILE
		

		if not sender or not receiver or not amt:
			print("transaction error 1")
			return False

		transaction = Transaction(sender, receiver, amt)

		if not transaction.signTransaction(senderKey):
			return False

		if not transaction.isValidTransaction():
			print("transaction error 2")
			return False
		self.pendingTransactions.append(transaction)
		return len(self.chain) + 1

	def getLastBlock(self):

		return self.chain[-1]

	def addGenesisBlock(self):
		tArr = []
		tArr.append(Transaction("me", "you", 10))
		genesis = Block(tArr, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), 0)

		genesis.prev = "None"
		return genesis

	def isValidChain(self):
		for i in range(1, len(self.chain)):
			b1 = self.chain[i-1]
			b2 = self.chain[i]

			if not b2.hasValidTransactions():
				print("error 3")
				return False

			if b2.hash != b2.calculateHash():
				print("error 4")
				return False


			if b2.prev != b1.hash:
				print("error 5")
				return False
		return True

	# def generateKeys(self):
	# 	key = RSA.generate(2048)
	# 	private_key = key.export_key()
	# 	file_out = open("private.pem", "wb")
	# 	file_out.write(private_key)

	# 	public_key = key.publickey().export_key()
	# 	file_out = open("receiver.pem", "wb")
	# 	file_out.write(public_key)
		
	# 	print(public_key.decode('ASCII'))
	# 	return key.publickey().export_key().decode('ASCII')


		
	def getBalance(self, person):
		balance = 0 
		for i in range(1, len(self.chain)):
			block = self.chain[i]
			try:
				for j in range(0, len(block.transactions)):
					transaction = block.transactions[j]
					if(transaction.sender == person):
						balance -= transaction.amt
					if(transaction.receiver == person):
						balance += transaction.amt
			except AttributeError:
				print("no transaction")
		return balance + 100


class Block ():
	def __init__(self, transactions, time, index):
		self.index = index
		self.transactions = transactions
		self.time = time
		self.prev = ''
		self.nonse = 0
		self.hash = self.calculateHash()


	def calculateHash(self):

		hashTransactions = ""

		for transaction in self.transactions:
			hashTransactions += transaction.hash
		hashString = str(self.time) + hashTransactions + self.prev + str(self.nonse)
		hashEncoded = json.dumps(hashString, sort_keys=True).encode()
		return blake3(hashEncoded).hexdigest()

	def mineBlock(self, difficulty):
		arr = []
		for i in range(0, difficulty):
			arr.append(i)
		
		#compute until the beginning of the hash = 0123..difficulty
		arrStr = map(str, arr)  
		hashPuzzle = ''.join(arrStr)
		
		while self.hash[0:difficulty] != hashPuzzle:
			print("Please Hold On, ⛏️⛏️⛏️ MINING BLOCK ⛏️⛏️⛏️ \n")
			self.nonse += 1
			self.hash = self.calculateHash()
			
		print("Block Mined!")
		return True

	def hasValidTransactions(self):
		for i in range(0, len(self.transactions)):
			transaction = self.transactions[i]
			if not transaction.isValidTransaction():
				return False
			return True
	
	
class Transaction ():
	def __init__(self, sender, receiver, amt):
		self.sender = sender
		self.receiver = receiver
		self.amt = amt
		self.time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") #change to current date
		self.hash = self.calculateHash()


	def calculateHash(self):
		hashString = self.sender + self.receiver + str(self.amt) + str(self.time)
		hashEncoded = json.dumps(hashString, sort_keys=True).encode()
		return blake3(hashEncoded).hexdigest()
		

	def isValidTransaction(self):
		#VERIFY TRANSACTION
		if(self.hash != self.calculateHash()):
			return False
		if(self.sender == self.receiver):
			return False
		if(self.sender == "Miner Rewards"):
			#security : unfinished
			return True
		#Using Public Key to verify 
		msg = str(self.amt).encode()
		public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve=ecdsa.SECP256k1)
		print("\n")
		print(public_key)
		print("\n")
		#print("msg", msg)
		verify = public_key.verify(self.signature, msg)
		if not self.signature or not verify:
			print("Signature Invalid")
			return False
		return True
		
	def signTransaction(self, senderKey):
		msg = str(self.amt).encode()
		print("msg", msg)
		print("\n")
		private_key = ecdsa.SigningKey.from_string(bytes.fromhex(senderKey), curve=ecdsa.SECP256k1)
		if(self.hash != self.calculateHash()):
			print("transaction tampered error")
			return False
		# Signing Transaction
		print("private_key", private_key)
		self.signature = private_key.sign(msg)
		
		return True