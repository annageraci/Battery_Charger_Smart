import pyfirmata
import time
if __name__ == '__main__':
    board = pyfirmata.Arduino("COM3")
    print("Communication Successfully started")

    it = pyfirmata.util.Iterator(board)
    it.start()

    board.digital[10].mode = pyfirmata.INPUT
    
    while True:
        board.digital[8].write(1)
        time.sleep(0.5)
        state = board.digital[10].read()
        print(state)
        time.sleep(0.5)
        board.digital[8].write(0)
        time.sleep(0.5)
        state = board.digital[10].read()
        print(state)
        time.sleep(0.5)