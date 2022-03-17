import time

from lib.threadRX import RX
from lib.threadTX import TX
from lib.interface import Interface


class Thread:
    def __init__ (self, name:str):
        self.interface = Interface(name)
        self.rx = RX(self.interface)
        self.tx = TX(self.interface)


    def enable (self):
        self.interface.open()
        time.sleep(0.1)
        self.rx.enable()
        self.tx.enable()
        print('Serial port enabled.')


    def disable (self):
        self.rx.disable()
        self.tx.disable()
        time.sleep(0.1)
        self.interface.close()
        print('Serial port disabled.')


    def clear (self):
        self.rx.clear()
        self.tx.clear()


    def transmit (self, *args, **kwargs):
        return self.tx.transmit(*args, **kwargs)


    def receive (self, *args, **kwargs):
        return self.rx.receive(*args, **kwargs)