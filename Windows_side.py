import socket
import logging
#import threading
#import Queue


class Handlers:
    def __init__(self):
        self.handlersDict = {}

    def set_socket_handler(self, socName, socObj):
        self.handlersDict[socName] = socObj

    def get_socket_handler(self, socName):
        return self.handlersDict[socName]

hand = Handlers()



def open_socket_management():
    '''
    Open a Socket for management

    :return: True\False
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((DST_TCP_IP, DST_TCP_PORT_MNGT))
    hand.set_socket_handler(socName=MNG_SOCKET, socObj=s)

def open_socket_data():
    '''
    Open a Socket for Data IMU\Image

    :return: True\False
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((DST_TCP_IP, DST_TCP_PORT_DATA))
    hand.set_socket_handler(socName=DATA_SOCKET, socObj=s)

def send_message(message):
    '''
    Send Management Message

    :return: True\False
    '''

    mng = hand.get_socket_handler(MNG_SOCKET)

    mng.send(message)


def recieve_message(num):
    '''
    Receive management message
    :return: Message
    '''
    mng = hand.get_socket_handler(MNG_SOCKET)
    data = mng.recv(BUFFER_SIZE)
    #print data
    f = open("c:\\temp\\elad_{0}.png".format(str(num)), "wb")
    f.write(data)


def init():

    '''
    open socket management
    open socket data
    open camera
    open imu
    start transmit data

    :return: True\False
    '''
    try:
        open_socket_management()
    except Exception as e:
        logger.error("{0} - port {1}".format(e, str(DST_TCP_PORT_MNGT)))


    try:
        open_socket_data()
    except Exception as e:
        logger.error("{0} - port {1}".format(e, str(DST_TCP_PORT_DATA)))



def destroy():
    '''
    stop transmit data
    close imu
    close camera
    close socket data
    close socket management

    :return: True\False
    '''
    mng = hand.get_socket_handler(MNG_SOCKET)
    data = hand.get_socket_handler(DATA_SOCKET)
    mng.close()
    data.close()

def ethernet_packets():
    """

    :return:
    """
    #metadata = [GAIN, RESOLUTION, EXPOSURE]
    data = []
    Image = open("H:\\Users\\Tamari\\2018-06-24.png", "rb")
    g = Image.read()
    b = bytearray(g)
    return b


def main():
    try:
        init()
    except:
        raise

    count = 0
    frameBuffer = {}

    while 1:
        count += 1
        t =  ethernet_packets()

        if t == "" and t == None:
            continue

        frameBuffer[count] = t
        send_message(t)
        recieve_message(count)

    destroy()

if __name__ == '__main__':
    DST_TCP_IP = '192.168.1.92'
    DST_TCP_PORT_MNGT = 5005
    DST_TCP_PORT_DATA = 5006
    BUFFER_SIZE = 3000000
    MNG_SOCKET = 'mngSocket'
    DATA_SOCKET = 'dataSocket'

    logger = logging.getLogger('eth_traffic')
    logger.setLevel(logging.DEBUG)
    # create file handler that logs debug and higher level messages
    fh = logging.FileHandler('ethLogger.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)


    main()









