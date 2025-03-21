from blockchain import Blockchain

# Create a new blockchain
my_blockchain = Blockchain()

my_blockchain.add_transaction("Alice", "Bob", 50)
my_blockchain.add_transaction("Bob", "Charlie", 30)

my_blockchain.mine_pending_transactions("miner_address")

my_blockchain.add_transaction("Charlie", "Alice", 20)
my_blockchain.add_transaction("Bob", "Alice", 10)

my_blockchain.mine_pending_transactions("miner_address")

print("Alice's balance:", my_blockchain.get_balance("Alice"))
print("Bob's balance:", my_blockchain.get_balance("Bob"))
print("Charlie's balance:", my_blockchain.get_balance("Charlie"))
print("Miner's balance:", my_blockchain.get_balance("miner_address"))

print("\nBlockchain valid?", my_blockchain.is_chain_valid())
