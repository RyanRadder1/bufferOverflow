import struct
import os
import argparse
import pprint
from ast import literal_eval
import time
import binascii

import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format


endian = "<"
junk = ""



# Disable output
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore output
def enablePrint():
    sys.stdout = sys.__stdout__



def pack(address):

    global endian

    #example
    #
    #packed = struct.pack('<L',0x0886fda1 )
    #

    packed = struct.pack(endian+'L', literal_eval(address))

    return packed


def Main():


    #build arguments
    parser= argparse.ArgumentParser()
    parser.add_argument('-a','--address', help="The memory address you wish to pack", type=str)
    parser.add_argument('-f' ,'--filename', help="The filename you wish to export to <FILENAME>.txt", type=str)
    parser.add_argument('-jf', '--junkfile', help="File location of junk", type=str)
    parser.add_argument('-j', '--junk', help="Enter junk prefix before address", type=str)
    parser.add_argument('-aj', '--afterjunk', help="Enter junk after address", type=str)
    parser.add_argument('-e', '--endian', help="Little(L) or big(B) endian defualt is Little endian", type=str)
    parser.add_argument('-s', '--silent', help="Suppresses all output except packed output (for direct input)",action="store_true" )

    args = parser.parse_args()

    if(args.silent):
        blockPrint()


    #Start program
    cprint(figlet_format('Makultr packer'),'yellow', 'on_red', attrs=['bold'])
    print("Starting packer script \nWritten by Makultr\n")
    if not(args.silent):
        time.sleep(1)


    global junk
    global endian
    if(args.endian):
        if(args.endian == "L"):
            print("user selected little endian\n")
            endian = "<"
        elif(args.endian == "B"):
            print("user selected big endian\n")
            endian = ">"
        else:
            pprint.pprint("wrong endian selection, defaulting to little endian \n")


    if(args.junkfile):
        print("Reading junk from : "+args.junkfile+"\n")
        fileExists = os.path.exists(args.junkfile)

        if(fileExists):
            f  = open(args.junkfile, 'r')
            junk = f.read()
            print("file found!\n\nReading file...\n\n"+"file content: "+junk)
        else:
            print("file not found \n")

    if(args.junk):
        print("using junk input : "+args.junk+"\n")
        if "*" in args.junk:
            splitJunk = args.junk.split("*")
            junk = splitJunk[0] * int(splitJunk[1])
        else:
            junk = args.junk


    if(args.address):
        print("packing...\n\n")
        packedAddr = pack(args.address)
        packed = junk+packedAddr
    else:
        packed = junk

    if(args.afterjunk):
        if "*" in args.afterjunk:
            splitJunk = args.afterjunk.split("*")
            afterjunk = splitJunk[0] * int(splitJunk[1])
        else:
            afterjunk = args.afterjunk
        packed += afterjunk


    if not(args.silent):
        print("packed output: "+packed+"\n\n")

    if(args.filename):
        print("writing to file: "+args.filename+".txt...\n")
        f = open(args.filename+".txt", "w")
        f.write(packed)
        f.close()
        print("done writing to file")


    if(args.silent):
        enablePrint()
        reload(sys)
        sys.setdefaultencoding("ascii")
        sys.stdout.write(packed)




if __name__ == "__main__":
    Main()
