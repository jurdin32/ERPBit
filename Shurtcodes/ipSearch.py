# -*- coding: utf-8 -*-
import socket, subprocess
from urllib.request import urlopen
import re
from uuid import getnode as get_mac

def getLocalIP():
    data=[i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]
    print(data)
    for ip in data:
        print("Datos: ",ip)
    return data

def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'
    ip=re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
    print(data)
    print("Su IP Publica es: ",ip)
    return ip


def obtenerMac():
    mac = get_mac()
    mac = ':'.join(("%012X" % mac)[i:i + 2] for i in range(0, 12, 2))
    print ('MAC >>>: ', mac)
getLocalIP()
obtenerMac()
getPublicIp()