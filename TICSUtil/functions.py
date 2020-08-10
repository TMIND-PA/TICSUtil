from datetime import datetime
import configparser
from cryptography.fernet import Fernet
from getmac import get_mac_address
import socket

def log_time():
    """ Returns date time with ms. Can be used for logging messages"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def readconfigfile(filename,section,key):
    # root = ".\TICSEvtMgr"
    # filename = os.path.join(root,filename)
    config = configparser.ConfigParser()
    config.read(filename,  encoding='utf-8')
    return config.get(section, key)

def decrypt(password):
    encoded_key = b'U3FidkxCQ1dMSFBtcTZwU3VjVnFlaFNQRU45RHQwOGJ2azFScG0wT2ZaWT0=\n'
    key = base_decode(encoded_key)
    f = Fernet(key)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    mac = get_mac_address()
    if password.__class__ == str:
        token = f.decrypt(password.encode('utf-8'))
    else:
        token = f.decrypt(password)
    output = token.decode("utf-8").replace(ip + mac, '')
    return output