from datetime import datetime
import configparser, inspect, base64, json, rsa, psutil, os
from base64 import b64decode
from cryptography.fernet import Fernet
from getmac import get_mac_address
from ipaddress import IPv4Address

def log_time():
    """ Returns date time with ms. Can be used for logging messages"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

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

def alarm_internal(rclient, alm_channel="alarm_queue", tag="internal", msg="", priority="Low", value=0):
    func_name = inspect.stack()[1].function
    alm_ts = str(datetime.now())
    alm_data = {"alm_tag":tag ,"value":value, "alm_name":func_name, "alm_desc":msg, "alm_priority":priority, "alm_ts":alm_ts, "pd":process_data}
    rclient.publish(alm_channel, json.dumps(alm_data))

def get_mac_all(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield snic.address

def check_license(config_file, application):
    status = 0
    license_path = readconfigfile(config_file,'license', 'path')
    filename = readconfigfile(config_file,'license', 'file')
    license_file= os.path.join(license_path, filename)
    # Log.info(f'License file path:{license_file}')
    if os.path.exists(license_file):
        config = configparser.ConfigParser()
        config.read(license_file,  encoding='utf-8')
        if 'license' in config:
            section = config['license']
            if 'application' in section and 'customer' in section and \
                'reference' in section and 'expire' in section and 'key' in section:
                pubkey = rsa.PublicKey(7514513144282372129647063215394916456869398537697968821675421023637195249518021134485320680971729707960684956187071298549155245246725650219448549812838423, 65537)
                addr = get_mac_all(psutil.AF_LINK)
                for mac in addr:
                    data =  mac + section['application'] + section['customer'] + section['reference'] + section['expire']
                    try:
                        rsa.verify(data.encode('utf-8'), b64decode(section['key'].encode()), pubkey)
                    except Exception as e:
                        msg = str(e)
                    else:
                        status = 1
                        break
                if status < 1:
                    msg = f'This license is invalid for this machine'
                    return status, None, None, None, msg
                else:
                    if datetime.strptime(section['expire'], '%Y-%m-%d').date() >= datetime.now().date():
                        if application==section['application']:
                            status = 1
                            msg = f"License key Registed to {section['customer']} for Application: {section['application']} valid till: {section['expire']}"
                            return status, section['application'], section['customer'], section['expire'], msg
                        else:
                            status = 101
                            msg = f'License is not valid for the application'
                            return status, section['application'], section['customer'], section['expire'], msg
                    else:
                        status = 102
                        msg = f"License expired on {section['expire']}"
                        return status, section['application'], section['customer'], section['expire'], msg
            else:
                msg = f'Invalid license file'
                status = 103
                return status, None, None, None, msg
        else:
            msg = f'Invalid license file'
            status = 104
            return status, None, None, None, msg
    msg = f'License file not found'
    status = 6
    return status, None, None, None, msg