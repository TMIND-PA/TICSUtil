from datetime import datetime
import configparser, socket, base64, inspect
from cryptography.fernet import Fernet
from getmac import get_mac_address
from ipaddress import IPv4Address

def log_time():
    """ Returns date time with ms. Can be used for logging messages"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def readconfigfile(filename,section,key):
    config = configparser.ConfigParser()
    config.read(filename,  encoding='utf-8')
    return config.get(section, key)

def writeconfigfile(filename,section,key,value):
    config = configparser.ConfigParser()
    config.read(filename,  encoding='utf-8')
    config.set(section, key, value)
    with open(filename, 'w') as configfile:
        config.write(configfile)
        
def decrypt(password, ipaddress):
    encoded_key = b'U3FidkxCQ1dMSFBtcTZwU3VjVnFlaFNQRU45RHQwOGJ2azFScG0wT2ZaWT0=\n'
    key = base64.decodebytes(encoded_key)
    f = Fernet(key)
    try:
        IPv4Address(ipaddress)
        mac = get_mac_address(ip=ipaddress)
        # space in password not allowed
        if ' ' in password:
            output = None
        else:
            if password.__class__ == str:
                token = f.decrypt(password.encode('utf-8'))
            elif password.__class__ == bytes:
                token = f.decrypt(password)
            else:
                password = str(password)
                token = f.decrypt(password.encode('utf-8'))
            if token.decode("utf-8").find(mac) != -1:
                output = token.decode("utf-8").replace(mac, '')
            else:
                output = None
    except Exception as e:
        output = None
    return output

def alarm_internal(rclient, tag='internal', msg='', priority='Low', value=0):
    func_name = inspect.stack()[1].function
    alm_ts = str(datetime.now())
    alm_data = {'alm_tag':tag ,'value':value, 'alm_name':func_name, 'alm_desc':msg, 'alm_priority':priority, 'alm_ts':alm_ts}
    rclient.publish('alarm_queue', str(alm_data))

def get_config_db(session, tablename):
    result =dict()
    db_class = globals()[tablename]
    try:
        columns = [column.name for column in db_inspect(db_class).c]
        table_pk = db_class.__pkCol__
        rows = session.query(db_class).all()
        for row in rows:
            row_dict = row.__dict__
            temp_dict = dict()
            for item in columns:
                if item != table_pk:
                    temp_dict[item] = row_dict[item]
            result[row_dict[table_pk]] = temp_dict
    except Exception as e:
        print(f'Error in getting config from DB, msg:{e}')
    return result
