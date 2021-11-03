#!/usr/bin/env python3

from zlib import crc32
import struct
import sys

"""
Brute force the image dimensions of a PNG image.
"""

usage = f"usage : {sys.argv[0]} IMAGE"

if len(sys.argv) != 2:
    print(usage)
    exit()
try:
    png = bytearray(open(sys.argv[1], 'rb').read())
except:
    print(f"[-] No such file or directory : {sys.argv[1]}")
    exit()

# Pull the crc
crcStart = 29
crcTarget = png[crcStart:crcStart+4]

for width in range(1500):
    for height in range(1500):

        png[0x10:0x14] = struct.pack(">I",width)
        png[0x14:0x18] = struct.pack(">I",height)

        calculatedCrc = crc32(png[12:29]) & 0xffffffff
        if struct.pack('!I', calculatedCrc) == crcTarget:
            print('[+] Found Correct Dimensions...\n[+] Width: {}\n[+] Height: {}'.format(hex(width),hex(height)))
            with open('fixed.png','wb') as file:
                file.write(png)
            print('\n[+] Successfully wrote to: fixed.png')
            exit()

print("Can't found correct dimensions :(")