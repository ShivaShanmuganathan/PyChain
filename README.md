# PyChain

## :snake: Building a Blockchain from scratch in Python.
### :link: I built this Blockchain in Python to better understand how a Blockchain works

## :rocket: Features

1. How a transaction is added to a block
2. How a transaction is validated before adding 
3. How a block is added to blockchain
4. How a block is validated before adding
5. What is mining, proof of work and how it works
6. How to perform hashing on transaction and block
7. How to sign and verify and transaction
8. How a miner gets rewarded 

## :rocket: Features Yet to be Added
I still need to work on distributed consensus part.

## Dockerized Local Blockchain built in Python
## 🛸How to run?

### After Cloning the Repository

## Step 1: Build The Docker Image

  ```sh
  docker build -t pychain .
  ```
## Step 2: Start The Docker Container

  ```sh
  docker run --name pyblocks pychain
  ```



#### If you are unable to see emojis in the output, try running the container from the terminal of code editor (Works in VS Code)
------------------------------------------------------------------------------------------------------------------------------------

## :mag: How does it work?

### Run.py 
1. Generate Keys for sender1, sender2, receiver, and miner
2. Create the blockchain
3. Add Transaction [Sender1 sends money to Receiver]
4. Add another Transaction [Sender2 sends money to Receiver]
5. Miner validates the pending transactions, adds the transaction to a block, mines the block, and adds it to the Blockchain
6. We can see the status of the Blockchain
7. We can see the account balance of the Receiver

