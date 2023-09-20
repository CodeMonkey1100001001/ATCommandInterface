# master.py # 20220603.2034
import os
import time
import random
import usb_cdc
swVersion = "+AT Commands on CircuitPython v20230919.1925"

serialBuffer = bytearray(512)
serialBufferPointer = 0
serialBufferLen = len(serialBuffer)

incomingCommand = ""

knownCommands = {
    "+ID": "id",
    "+INFO": "info",
    "+CCLK": "cclk",
    "+RAND": "make_rand",
    "?": "help"
}


def doNothing(ignoreme):
    return True


def printSerial(whatToPrint):
    print(whatToPrint, end='\r\n')


def id(arguments):
    global uart, swVersion
    print("+ID: "+swVersion)
    print('+IDOS: ' + str(os.uname()) + "\r\n")
    return True


def help(arguments):
    print("+Known Commands")
    for oneCommand in knownCommands:
        print(oneCommand)


def make_rand(arguments):
    print("+Arguments[" + arguments + "]")
    print(arguments[1:])
    maxValue = getInt(arguments)
    if (maxValue < 0):
        maxValue = 10
        print("+INFO MaxValue invalid using 10")
    print("+MaxValue = " + str(maxValue))
    print("+MinValue = 0")
    print("+Rand = " + str(random.randint(0, maxValue)))
    return True


def info(arguments):
    print("info requested")
    print("Is this the info you want?")
    return True


def cclk(arguments):
    print("+INFO: time requested")
    timeNow = "+" + str(time.monotonic())
    print(timeNow)
    return True


#####################
def hexDumpStr(theStr):
    # print("hexdump_type",type(theStr))
    for character in theStr:
        print(hex(ord(character)), end='')
    print()


def getInt(inStrVal):
    # hexDumpStr(inStrVal)
    retInt = -1
    try:
        retInt = int((inStrVal))
    except:
        retInt = -1
        print("Error converting Int[" + str(inStrVal) + "]")
    return retInt


def serialBufferToString():
    global serialBuffer, serialBufferPointer
    returnValue = ""
    i = 0
    for i in range(0, serialBufferPointer):
        # print("i",i,"=",chr(serialBuffer[i]))
        returnValue += chr(serialBuffer[i])
    return returnValue.upper()


def serialBufferFlush():
    global serialBuffer, serialBufferPointer
    i = 0
    while i < len(serialBuffer):
        serialBuffer[i] = 0x00
        i += 1
    serialBufferPointer = 0


def parseIncomingTry(theCommand):
    retV = False
    try:
        retV = parseIncoming(theCommand)
    except:
        print("Error processing incoming")
        return False
    return retV


def parseIncoming(theCommand):
    global knownCommands
    # print("type_theCommand",type(theCommand),theCommand)
    if (len(theCommand) < 3):
        if theCommand == "AT":
            return True
        return False
    # print ("theCommand["+theCommand+"]")

    aMatch = 0
    doCommand = ""
    arguments = ""

    for i in knownCommands:
        # print("i=",i,"func=",knownCommands[i])
        aMatch = compareCommand(i, theCommand)
        if (aMatch >= 1):
            doCommand = knownCommands[i]
            if (len(i) + 1 >= len(theCommand)):
                arguments = ""
            else:
                arguments = theCommand[len(i) + 3:]
                arguments = arguments.rstrip()
                if (aMatch == 2):
                    arguments = theCommand
            # print("command Match",i,"doCommand",doCommand,"aMatch",aMatch)
    if len(doCommand) > 0:
        globals()[doCommand](arguments)
    else:
        print("ERROR")
        return False

    return True


def compareCommand(needle, haystack):
    # _ underscore is a wildcard for numeric values
    retV = 0
    wildCardMatch = 0
    # print("needle:",needle)
    # print("haystack:",haystack)
    startPos = 2  # ignore the AT and any space
    # print("startPos:",startPos)
    compareLen = len(needle)
    # print("compareLen",compareLen)
    for i in range(0, compareLen):
        # print("i=",i)
        if (i + startPos >= len(haystack)):
            haystackChar = "*"
        else:
            haystackChar = haystack[i + startPos]
        needleChar = needle[i]
        # print("needleChar["+needleChar+"] haystackChar["+haystackChar+"]")
        if (needleChar == haystackChar):
            retV = retV + 1
            # print("hit")
        else:
            # print("hs["+haystack[i+startPos]+"]")
            if (needle[i] == '_' and haystackChar.isdigit()):  # >='0' and haystackChar <='9'):
                retV = retV + 1
                wildCardMatch = 1

    # print("compareLen",compareLen,"retV",retV)
    if (compareLen == retV):
        retV = 1
    else:
        retV = 0

    if (retV == 1) and (wildCardMatch == 1):
        retV = 2

    return retV

def doOtherStuff(timeNow):
    global tickTime
    if timeNow - tickTime > 10:
        print("+INFO: Tick", timeNow)
        tickTime = timeNow


# ----------------------------
# Main Code begins here
# ----------------------------
print("+BOOT")
id('')
print("OK")

buffer = ""
serial = usb_cdc.console

oldTime = time.monotonic()
runStart = oldTime
tickTime = oldTime

while True:
    now = time.monotonic()
    doOtherStuff(now)
    oldTime = now
    while serial.in_waiting:
        inByte = serial.read(1)
        # print("["+chr(inByte[0])+"]", end='')
        print(chr(inByte[0]), end='')
        serialBuffer[serialBufferPointer] = inByte[0]
        serialBufferPointer += 1
        if (inByte[0] == 0x0D or serialBufferPointer >= serialBufferLen):
            print("")  # flush output to terminal
            # print("")  # flush local output
            # print("==============CR============")
            # incomingCommand = serialBuffer.decode()
            incomingCommand = serialBufferToString()
            incomingCommand = incomingCommand.rstrip()

            serialBufferFlush()
            # print("incoming Command["+incomingCommand+"]")
            # procCmdRet = processCommand(incomingCommand)
            # procCmdRet = parseIncoming(incomingCommand)
            procCmdRet = parseIncomingTry(incomingCommand)
            if (procCmdRet == 1):
                print("OK\r\n")
            else:
                print("ERROR\r\n")
