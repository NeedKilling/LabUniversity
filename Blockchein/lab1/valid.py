
def checkChain(chain):
    valid = True
    
    if(chain[0].hash != chain[0].createHash()):
            print(f"Ошибка хеша в блоке {chain[i].index}")
            valid = False
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


def checkPow(chain):
    # zeroLine = '0' * dif
    valid = True
    for block in chain:
        zeroLine = '0' * block.difficulty
        if not block.hash.startswith(zeroLine):
            print(f"Ошибка PoW в блоке {block.index}: хеш {block.hash} не начинается с {zeroLine}")
            valid = False
    if valid:
        print("\tВсе блоки прошли проверку PoW")
    else:
        print("\tНекоторые блоки не прошли проверку PoW")
