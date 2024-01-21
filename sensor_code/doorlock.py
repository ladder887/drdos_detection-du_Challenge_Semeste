import RPi.GPIO as GPIO
from datetime import datetime


Doorpin = 3
Buttons = [0x300ff4ab5, 0x300ff6897, 0x300ff9867, 0x300ffb04f, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff52ad]
ButtonsNames = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', 'shop']
doorlock = '77091230'
door = ''

GPIO.setmode(GPIO.BCM)
GPIO.setup(Doorpin, GPIO.IN)

def getBinary():
    numls = 0
    binary = 1
    command = []
    previousValue = 0
    value = GPIO.input(Doorpin)
    
    while value:
        value = GPIO.input(Doorpin)
        
    startTime = datetime.now()
    
    while True:
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime
            startTime = now
            command.append((previousValue, pulseTime.microseconds))
        
        if value:
            numls += 1
        
        else:
            numls = 0
        
        if numls > 10000:
            break
        
        previousValue = value
        value = GPIO.input(Doorpin)
        
    for (typ, tme) in command:
        if typ == 1:
            if tme > 1000:
                binary = binary * 10 + 1
                
            else:
                binary *= 10
        
    if len(str(binary)) > 34:
        binary = int(str(binary)[:34])
    
    return binary

def convertHex(binaryValue):
    tmpB2 = int(str(binaryValue), 2)
    
    return hex(tmpB2)

def lockon(door):
    global doorlock
    #print('doorlock = ', doorlock)
    #print('door = ', door)
    if doorlock == door:
        print('unlock')

    else:
        print('false')


while True:
    inDate = convertHex(getBinary())
    
    for button in range(len(Buttons)):
        if hex(Buttons[button]) == inDate:
            print(ButtonsNames[button])
            
            if button == 10:
                lockon(door)
                door = ''
            else:
                door += str(button)
                #print(door)
            
            