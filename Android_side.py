import socket
import logging
from multiprocessing import Pool, Process

class Handlers:
    def __init__(self):
        self.handlersDict = {}

    def set_socket_handler(self, socName, socObj):
        self.handlersDict[socName] = socObj

    def get_socket_handler(self, socName):
        return self.handlersDict[socName]

hand = Handlers()

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

def start_listen_mng(xlist):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((xlist[0], int(xlist[1])))
    s.listen(1)

    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(xlist[2])
        #data = ethernet_packets()
        if not data: break
       # logger.info("received data:", data)
        conn.send(data)  # echo

def ethernet_packets():
    """

    :return:
    """
    #metadata = [GAIN, RESOLUTION, EXPOSURE]
    data = []
    Image = open("H:\\Users\\Tamari\\2018-06-24.png", "rb")
    g = Image.read()
    return g


def main():
    pool = Pool(2)
    xlist = [(DST_TCP_IP, DST_TCP_PORT_MNGT, BUFFER_SIZE)]

    pool.map(start_listen_mng, xlist )

    #destroy()

if __name__ == '__main__':
    #ethernet_packets()
    DST_TCP_IP = '192.168.1.92'
    DST_TCP_PORT_MNGT = 5005
    DST_TCP_PORT_DATA = 5006
    BUFFER_SIZE = 40096
    MNG_SOCKET = 'mngSocket'
    DATA_SOCKET = 'dataSocket'
    GAIN = "1"
    RESOLUTION = "1280x960"
    EXPOSURE = "200"


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