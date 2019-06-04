import hashlib

MAX_ITERS = pow(10, 5)

class transaction:
    def __init__(self, from_addr, to_addr, amount):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount


class block:
    def __init__(self, timestamp, transactions, previous_hash=''):
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.nonce = 0
        self.transactions = transactions 
        self.hash = self.calc_hash()
        

    def mine(self, difficulty):
        for i in range(MAX_ITERS):
            self.nonce += 1
            self.hash = self.calc_hash()
            if self.hash.startswith('0' * difficulty):
                print('block mined', self.hash)
                break

    def calc_hash(self):
        return str(hashlib.sha256(str(self.transactions) + str(self.previous_hash) + str(self.timestamp) + str(self.nonce) ).hexdigest())


class blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.mining_reward = 100

    def get_balance(address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.from_addr == address:
                    balance -= tx.amount

                if tx.to_addr == address:
                    balance += tx.amount

        return balance

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, mining_reward_address):
        b = block(1234, self.pending_transactions, self.get_latest_block().hash)
        b.mine(2)
        self.chain.append(b) 
        self.pending_transactions = [transaction(None, mining_reward_address, self.mining_reward)]

    def create_genesis_block(self):
        return block('01/01/1970', 'genesis block', '0')

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def add_block(self, new_block, difficulty):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine(difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
                current_block = self.chain[i]
                previous_block = self.chain[i-1]

                if current_block.hash != current_block.calc_hash():
                    print('1st')
                    return False

                if current_block.previous_hash != previous_block.hash:
                    print('2nd')
                    print('i = ', i)
                    print('current->previous', current_block.previous_hash)
                    print('previous', previous_block.hash)
                    return False


                return True # entire chain consistent    
        return True #chain with genesis_block only


    

bc = blockchain()
bc.create_transaction(transaction('addr1', 'addr2', 100))
bc.create_transaction(transaction('addr2', 'addr1', 50))
bc.mine_pending_transactions('receiver address')
print('len bc', len(bc.chain))
print('checking consistency', bc.is_chain_valid())

