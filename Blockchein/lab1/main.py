import hashlib
import time

class Block:
    def __init__(self, index, data, previousHash, nonce):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previousHash = previousHash
        self.nonce = nonce
        self.hash = self.createHash()

    def createHash(self):
        hashText = f"{self.index}{self.timestamp}{self.data}{self.previousHash}{self.nonce}"
        hash = hashlib.sha256(hashText.encode())
        # print(f"create hash: {hash.hexdigest()}")
        return hash.hexdigest()





def createChain():
    first = Block(0, 'data0', 0, 0)

    chain = [first]

    previous = first.hash
    for item in range(1,5):
        block = Block(item, f'data{item}', previous, 0)
        chain.append(block)
        previous = block.hash

    return chain


def checkChain(chain):
    valid = True

    for i in range(1,len(chain)):
        if(chain[i].hash != chain[i].createHash()):
            print(f"Ошибка хеша в блоке {chain[i].index}")
            valid = False
        if(chain[i].previousHash != chain[i-1].hash):
            print(f"Ошибка связи между блоками {chain[i-1].index} и {chain[i].index}")
            valid = False


    if(chain[0].previousHash != 0):
        print("previous_hash нулевого элемента может быть только 0")
        valid = False

    if(valid):
        print("\tЦепь целостна")
    else:
        print("\tЦепь повреждена")




CHAIN = createChain()

#CHAIN[2].previousHash = "333" # тест проверки
# CHAIN[2].hash = "333" # тест проверки


for item in CHAIN:
    print(f"\nindex = {item.index} \ntimestamp = {item.timestamp}\ndata = {item.data}\npreviousHash = {item.previousHash}\nnonce = {item.nonce}\nhash = {item.hash}\n\n")


checkChain(CHAIN)