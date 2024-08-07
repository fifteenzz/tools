# coding=utf8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from multiprocessing import Pool
import  os,time,random
import re
import telnetlib



def host():
    #将host文件放在同目录
    with open('host') as myhost:
        url_base = myhost.read().splitlines()
        return url_base

def myrun(url_base):

    url_base_one = url_base.split(":")
    host_one = url_base_one[0]
    port_one = int(url_base_one[1])

    try:
        import socket
        import binascii
        host = host_one
        port = port_one
        # print(host)
        # print(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        hex1 = "000100010000000100000000"
        hex2 = "0000000000000001000000c5"
        hex3 = "6f00000000000000bc7b2276657273696f6e223a22302e33372e30222c22686f73746e616d65223a22222c226f73223a2277696e646f7773222c2261726368223a22616d643634222c2275736572223a22222c2270726976696c6567655f6b6579223a223339303037333863396338313762616234333835343866343861366432383233222c2274696d657374616d70223a313632393038323130392c2272756e5f6964223a22222c226d65746173223a6e756c6c2c22706f6f6c5f636f756e74223a317d"
        str = binascii.unhexlify(hex1)
        s.send(str)
        str = binascii.unhexlify(hex2)
        s.send(str)
        str = binascii.unhexlify(hex3)
        s.send(str)
        s.recv(12)
        s.recv(12)
        resp = s.recv(88)
        # print(resp)

        if b'error' not in resp:
            print("主机{}端口{}存在不鉴权".format(host,port))
    except:
        pass

if __name__ == "__main__":
    # 调整进程数量，越大扫描越快，建议为CPU内核数量
    print("扫描开始")
    p = Pool(20)
    hosts = host()
    for urlbase in hosts:
        p.apply_async(myrun,(urlbase,))

    p.close()
    p.join()
    print("扫描结束")

