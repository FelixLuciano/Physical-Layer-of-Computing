import binascii

import serial


class Interface:
    BAUDRATE = 115200
    # BAUDRATE = 57600
    # BAUDRATE = 38400
    # BAUDRATE = 31250
    # BAUDRATE = 28800
    # BAUDRATE = 19200
    # BAUDRATE = 14400
    # BAUDRATE = 9600
    # BAUDRATE = 4800
    # BAUDRATE = 2400
    # BAUDRATE = 1200
    # BAUDRATE = 600
    # BAUDRATE = 300
    BYTESIZE = serial.EIGHTBITS
    PARITY = serial.PARITY_NONE
    STOPBITS = serial.STOPBITS_ONE
    TIMEOUT = 0.1


    def __init__ (self, name:str):
        self.name = name
        self.port = None
        self.rxRemain = b''


    def open (self):
        self.port = serial.Serial(
            port = self.name,
            baudrate = self.BAUDRATE,
            bytesize = self.BYTESIZE,
            parity = self.PARITY,
            stopbits = self.STOPBITS,
            timeout = self.TIMEOUT
        )


    def close (self):
        self.port.close()


    def flush (self):
        self.port.flushInput()
        self.port.flushOutput()


    @staticmethod
    def encode (data:bytes):
        return binascii.hexlify(data)


    @staticmethod
    def decode (data:bytes):
        return binascii.unhexlify(data)


    def write (self, txBuffer:bytes):
        """ Write data to serial port

        This command takes a buffer and format
        it before transmit. This is necessary
        because the pyserial and arduino uses
        Software flow control between both
        sides of communication.
        """
        nTx = self.port.write(self.encode(txBuffer))

        self.flush()

        return nTx // 2


    def read (self, nBytes:int):
        """ Read nBytes from the UART com port

        Not all reading returns a multiple of 2
        we must check this to prevent the self.
        decode function from being called with
        odd numbers.
        """
        rxBuffer = self.port.read(nBytes)
        rxBufferConcat = self.rxRemain + rxBuffer
        nValid = (len(rxBufferConcat) // 2) * 2
        rxBufferValid = rxBufferConcat[0:nValid]

        self.rxRemain = rxBufferConcat[nValid:]

        try:
            """ Sometimes there are errors in decoding
            outside the linux environment, this tries
            to partially correct these errors. Improve
            in the future. often a flush at the
            beginning solves!
            """
            # self.flush()

            rxBufferDecoded = self.decode(rxBufferValid)
            nRx = len(rxBuffer)

            return rxBufferDecoded, nRx

        except:
            print('[ERROR] Physical interface, read, decode. buffer:\n', rxBufferValid)

            return b'', 0
