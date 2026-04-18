import hashlib
import time

class Block:
    def __init__(self, index, data, previousHash, difficulty = 3):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previousHash = previousHash
        self.difficuty = difficulty
        self.nonce = 0
        self.hash = self.createHash()

    def createHash(self):
        hashText = f"{self.index}{self.timestamp}{self.data}{self.previousHash}{self.nonce}"
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



def timeCreateBlock(block,dif):
    start = time.perf_counter()
    block.main(dif)
    end = time.perf_counter() - start
    return [block,end]
    



# def createChain(difficulty):
#     first = Block(0, 'data0', 0)
#     first.main(difficulty) #main


#     chain = [first]

#     previous = first.hash
#     for item in range(1,5):
#         block = Block(item, f'data{item}', previous)
#         block.main(difficulty) #main
#         chain.append(block)
#         previous = block.hash

#     return chain
def createChain(difficulty):
    first = timeCreateBlock(Block(0, 'data0', 0), difficulty)
    
    t = 0
    chain = [first]
    previous = first[0].hash

    for item in range(1,5):
        block = timeCreateBlock(Block(item, f'data{item}', previous),difficulty)
        chain.append(block)
        previous = block[0].hash
        t+=block[1]
        
        
    for item in chain:
        print(f"\tindex = {item[0].index} \n\ttimestamp = {item[1]:3f}\n\tpreviousHash = {item[0].previousHash}\n\tnonce = {item[0].nonce}\n\thash = {item[0].hash}\n\t--------------------------")
    print(f"full time : {t}")
    return chain


def checkChain(chain):
    valid = True
    
    if(chain[0][0].hash != chain[0][0].createHash()):
            print(f"Ошибка хеша в блоке {chain[i][0].index}")
            valid = False
    for i in range(1,len(chain)):
        if(chain[i][0].hash != chain[i][0].createHash()):
            print(f"Ошибка хеша в блоке {chain[i][0].index}")
            valid = False
        if(chain[i][0].previousHash != chain[i-1][0].hash):
            print(f"Ошибка связи между блоками {chain[i-1][0].index} и {chain[i][0].index}")
            valid = False


    if(chain[0][0].previousHash != 0):
        print("previous_hash нулевого элемента может быть только 0")
        valid = False
    if(valid):
        print("\tЦепь целостна")
    else:
        print("\tЦепь повреждена")


def checkPow(chain,dif):
    zeroLine = '0' * dif
    valid = True
    for block in chain:
        if not block[0].hash.startswith(zeroLine):
            print(f"Ошибка PoW в блоке {block[0].index}: хеш {block[0].hash} не начинается с {zeroLine}")
            valid = False
    if valid:
        print("\tВсе блоки прошли проверку PoW")
    else:
        print("\tНекоторые блоки не прошли проверку PoW")


def timeMine():
    for dif in [2,3,4]:
        testBlock = Block(0,"test",0)
        start = time.perf_counter()
        testBlock.main(dif)
        end = time.perf_counter() - start
        print(f"difficulty {dif} -   {end:3f}")



def createChains():
    for dif in [2,3,4]:
        print(f"\ndif ------- {dif}------------")
        chain = createChain(dif)
        checkChain(chain)
        checkPow(chain,dif)



createChains()

timeMine()
# CHAIN = createChain()


# for item in CHAIN:
#     print(f"\nindex = {item.index} \ntimestamp = {item.timestamp}\ndata = {item.data}\npreviousHash = {item.previousHash}\nnonce = {item.nonce}\nhash = {item.hash}\n")


# checkChain(CHAIN)


# timeMine()