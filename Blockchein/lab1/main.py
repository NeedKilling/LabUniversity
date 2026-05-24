import hashlib
import time
import copy

from valid import checkChain,checkPow

class Block:
    def __init__(self, index, data, previousHash, transactions, difficulty = 3):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previousHash = previousHash
        self.difficulty = difficulty
        self.nonce = 0
        self.transactions = transactions
        self.hash = self.createHash()
        

    def __repr__(self):
        return (f"Block(\n"
                f"  index={self.index},\n"
                f"  hash={self.hash},\n"
                f"  prev_hash={self.previousHash},\n"
                f"  data={self.data},\n"
                f"  nonce={self.nonce},\n"
                f"  difficulty={self.difficulty}\n"
                f")")

    def createHash(self):
        tx_str = "".join(str(tx.__dict__) for tx in self.transactions)
        hashText = f"{self.index}{self.timestamp}{self.data}{self.previousHash}{self.nonce}{tx_str}"
        hash = hashlib.sha256(hashText.encode())
        # print(f"create hash: {hash.hexdigest()}")
        return hash.hexdigest()
    
    def main(self,difficulty):
        zeroLine = "0" * difficulty

        while True:
            currentHash = self.createHash()
            if(currentHash.startswith(zeroLine)):
                self.hash = currentHash
                break
            self.nonce+=1

    def processBlock(self,state):
        snapshot = state.copy()
        for item in self.transactions:
            if not item.runTransaction(state):
                state.clear()
                state.update(snapshot)
                return False
                # return f"Ошибка в транзакции блока {self.index} {state}\n"
        return True
        # return f"Успешно {self.index} {state}\n"

class Transaction:
    def __init__(self, fromAddr, to, amount, payload=None):
        self.fromAddr = fromAddr 
        self.to = to              
        self.amount = amount        
        self.payload = payload      

    def contract(self, payload, state, fromAddr):
        if (payload is None):
            return True 
        if (payload["condition"] and payload["condition"] == "minBalance"):
            required = payload.get("value", 0)
            return state.get(fromAddr, 0) > required
        return False

    def runTransaction(self,state):
        if(state.get(self.fromAddr, 0) < self.amount):
            return False
        if(self.payload is not None):
            if not self.contract(self.payload, state, self.fromAddr):
                return False #/True
        state[self.fromAddr] -= self.amount
        state[self.to] = state.get(self.to, 0) + self.amount
        return True
    
    def __repr__(self):
        return f"Transaction(from={self.fromAddr}, to={self.to}, amount={self.amount}, payload={self.payload})"









def scenario():
    chain = []
    state = {"Alice": 1000, "Bob": 500, "Charlie": 200}
    print("=== Начальное состояние ===")
    print(f"{state}\n")

    def createBlock(index, data, transactions, previousHash,difficulty):
        block = Block(index, data , previousHash, transactions,difficulty)
        block.main(block.difficulty) 
        return block
    
    def applyBlock(block, state, chain):
        if block.processBlock(state):
            print(f"Блок {block.index} успешно. Состояние: {state}")
            chain.append(block)
            return True
        else:
            print(f"Ошибка в транзакции блока {block.index}. Блок откатили. Состояние: {state}")
            return False


    
    block1 = createBlock(1, "block1", [Transaction("Alice", "Bob", 100), Transaction("Bob", "Charlie", 50)], 0,3)

    contract_payload = {"condition": "minBalance", "value": 900} 
    block2 = createBlock(2, "block2",[Transaction("Alice", "Charlie", 10000, payload=contract_payload)], block1.hash,4)

    block3 = createBlock(3, "block3",[Transaction("Bob", "Charlie", 30),Transaction("Charlie", "Alice", 100)], block2.hash,3)

    


    for block in (block1, block2, block3):
        if not applyBlock(block, state, chain):
            break   

    # return [block1,block2,block3]
    return chain

chain = scenario()
if(chain):
    checkChain(chain)
    checkPow(chain)

print(chain)








# def timeCreateBlock(block,dif):
#     start = time.perf_counter()
#     block.main(dif)
#     end = time.perf_counter() - start
#     return [block,end]
    


# def createChain(difficulty):
#     first = timeCreateBlock(Block(0, 'data0', 0), difficulty)
    
#     t = 0
#     chain = [first]
#     previous = first[0].hash

#     for item in range(1,5):
#         block = timeCreateBlock(Block(item, f'data{item}', previous),difficulty)
#         chain.append(block)
#         previous = block[0].hash
#         t+=block[1]
        
        
#     for item in chain:
#         print(f"\tindex = {item[0].index} \n\ttimestamp = {item[1]:3f}\n\tpreviousHash = {item[0].previousHash}\n\tnonce = {item[0].nonce}\n\thash = {item[0].hash}\n\t--------------------------")
#     print(f"full time : {t}")
#     return chain


# def checkChain(chain):
#     valid = True
    
#     if(chain[0][0].hash != chain[0][0].createHash()):
#             print(f"Ошибка хеша в блоке {chain[i][0].index}")
#             valid = False
#     for i in range(1,len(chain)):
#         if(chain[i][0].hash != chain[i][0].createHash()):
#             print(f"Ошибка хеша в блоке {chain[i][0].index}")
#             valid = False
#         if(chain[i][0].previousHash != chain[i-1][0].hash):
#             print(f"Ошибка связи между блоками {chain[i-1][0].index} и {chain[i][0].index}")
#             valid = False


#     if(chain[0][0].previousHash != 0):
#         print("previous_hash нулевого элемента может быть только 0")
#         valid = False
#     if(valid):
#         print("\tЦепь целостна")
#     else:
#         print("\tЦепь повреждена")


# def checkPow(chain,dif):
#     zeroLine = '0' * dif
#     valid = True
#     for block in chain:
#         if not block[0].hash.startswith(zeroLine):
#             print(f"Ошибка PoW в блоке {block[0].index}: хеш {block[0].hash} не начинается с {zeroLine}")
#             valid = False
#     if valid:
#         print("\tВсе блоки прошли проверку PoW")
#     else:
#         print("\tНекоторые блоки не прошли проверку PoW")



# def createChains():
#     chains = []
#     for dif in [2,3,4]:
#         print(f"\ndif ------- {dif}------------")
#         chain = createChain(dif)
#         checkChain(chain)
#         checkPow(chain,dif)
#         chains.append(chain)
#     return chains

# createChains()


