import hashlib

MAX_ITERS = pow(10, 5)
class block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0
        self.hash = self.calc_hash()
        

    def mine(self, difficulty):
        for i in range(MAX_ITERS):
            self.nonce += 1
            self.hash = self.calc_hash()
            if self.hash.startswith('0' * difficulty):
                print('block mined', self.hash)
                break

    def calc_hash(self):
        return str(hashlib.sha256(str(self.index) + str(self.data) + str(self.previous_hash) + str(self.timestamp) + str(self.data) + str(self.nonce) ).hexdigest())


class blockchain:
    def __init__(self):
        self.chain = []
        self.chain.append(self.create_genesis_block())

    def create_genesis_block(self):
        return block(0, '01/01/1970', 'genesis block', '0')

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
                    return False

                if current_block.previous_hash != previous_block.hash:
                    return False


                return True # entire chain consistent    
        return True #chain with genesis_block only


    

data = ['xyz','abcxsadaasdasgawsz']
bc = blockchain()
b = block(1,2331,data)
b1 = block(1,2331,data)
bc.add_block(b, 3)
bc.add_block(b1, 3)
#adding the same block twice results in error while checking consistency
print('checking consistency', bc.is_chain_valid())

