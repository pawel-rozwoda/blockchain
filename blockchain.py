import hashlib
#hashed = hashlib.sha256(data).hexdigest()

class block:
    def __init__(self, index, timestamp, data, previous_hash=''):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.calc_hash()

    def calc_hash(self):
        return hashlib.sha256(str(self.index) + self.previous_hash + str(self.timestamp) + str(self.data))


class blockchain:
    def __init__(self):
        self.chain = []
        self.chain.append(self.create_genesis_block())

    def create_genesis_block(self):
        return block(0, '01/01/1970', 'genesis block', '0')

    def get_latest_block(self):
        return self.chain[len(self.chain) - 1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calc_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
                current_block = self.chain[i]
                previous_block = self.chain[i-1]

                if current_block.hash != current_block.calc_hash():
                    return False

                if current_block.previous_hash != previous_block.hash:
                    return False


                return True    
        return True


    

bc = blockchain()
print(bc.is_chain_valid())
b = block(1,2331,'xzasda', '4')
print(str({'x':'4'}))
