import hashlib
import json
import time
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, transactions: List[Dict[str, Any]], timestamp: float, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate the hash of the block."""
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 4  # Number of leading zeros required in hash
        self.pending_transactions: List[Dict[str, Any]] = []
        self.mining_reward = 10
        
        # Create genesis block
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Create the first block in the chain."""
        genesis_block = Block(0, [], time.time(), "0")
        self.mine_block(genesis_block)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Return the most recent block in the chain."""
        return self.chain[-1]

    def mine_block(self, block: Block) -> None:
        """Mine a block by finding a nonce that gives the required number of leading zeros."""
        target = "0" * self.difficulty
        
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()

    def add_block(self, transactions: List[Dict[str, Any]]) -> Block:
        """Create and add a new block to the chain."""
        latest_block = self.get_latest_block()
        new_block = Block(
            latest_block.index + 1,
            transactions,
            time.time(),
            latest_block.hash
        )
        
        self.mine_block(new_block)
        self.chain.append(new_block)
        return new_block

    def add_transaction(self, sender: str, recipient: str, amount: float) -> None:
        """Add a new transaction to the pending transactions list."""
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self, miner_address: str) -> None:
        """Mine pending transactions and add them to a new block."""
        # Add mining reward transaction
        self.pending_transactions.append({
            "sender": "network",
            "recipient": miner_address,
            "amount": self.mining_reward
        })
        
        # Create new block with pending transactions
        self.add_block(self.pending_transactions)
        self.pending_transactions = []

    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
                
            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True

    def get_balance(self, address: str) -> float:
        """Calculate the balance of a given address."""
        balance = 0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == address:
                    balance -= transaction["amount"]
                if transaction["recipient"] == address:
                    balance += transaction["amount"]
        
        return balance
