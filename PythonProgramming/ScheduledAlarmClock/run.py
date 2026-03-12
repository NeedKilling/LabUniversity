import sys
sys.dont_write_bytecode = True
from time import sleep
from handlers.message import messageHandler


if __name__ == "__main__":
    while(True):
        messageHandler()
        sleep(5)
