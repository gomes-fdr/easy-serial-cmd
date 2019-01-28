#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script para envio de comandos via serial.
# Autor: Fabiano da Rosa Gomes<gomes.fdr@gmail.com>
# Data: 20/12/2018

import serial
from hexdump import dump
from time import sleep
from math import fsum
from operator import xor

def calcSum(cmd):
    s = int(fsum(cmd))
    if s > 255:
        st = (s.to_bytes(4, byteorder='big'))
        return xor(st[-1], 0xff)
    return xor(s, 0xff)


ser = serial.Serial('/dev/ttyUSB0', 19200)

# Comandos de testes
tests = {
    'CN5 ': (b'\xa2\x01\x00\x54'),
    'CN4 ': (b'\xa2\x01\x00\x55'),
    'CN8 ': (b'\xa2\x01\x00\x56'),
    'CN9 ': (b'\xa2\x01\x00\x57'),
    'CN2 ': (b'\xa2\x01\x00\x58'),
    'CN1 ': (b'\xa2\x01\x00\x59'),
    'CN11': (b'\xa2\x01\x00\x5A'),
    'CN10': (b'\xa2\x01\x00\x5B'),
    'CN6 ': (b'\xa2\x01\x00\x5C'),
    'ID  ': (b'\xa2\x01\x02\x5D\x00\x00')
}

def main():
    while True:
        print('## Iniciando ciclo de testes... ##')
        for k, v in tests.items():
            cmd = (*v, calcSum(v), int(0x16))
            ser.write(cmd)
            ser.flushInput()
            print('Enviei[t_{0}]: {1}'.format(k, dump(bytearray(cmd))))
            if v[-1] == 0x54:
                rcv = ser.read(9)
            else:
                rcv = ser.read(7)

            print('Recebi:         ' + dump(rcv))
            sleep(3)
        print('---')
        print()

if __name__ == "__main__":
    main()
