import RPi.GPIO as GPIO
import time

IR_sensor = 4
LED = 17
switch = 15
state = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_sensor, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setup(switch, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def button_callback(channel):
    global state
    print('Button pushed!')
    state = not state
    
    if state == 1:
        GPIO.output(LED, state)
        print('ON', state)
    
    elif state == 0:
        GPIO.output(LED, state)
        print('OFF', state)
#   global state
#    state = not state
#    GPIO.output(LED, state)
    
GPIO.add_event_detect(switch, GPIO.RISING, callback=button_callback, bouncetime = 300)

while True:
    if state == 1:
        time.sleep(5)
    while state == 1:
        if GPIO.input(IR_sensor):
            GPIO.output(LED, state)
            print('IR sensing',state)
            time.sleep(5)
        else:
            GPIO.output(LED, GPIO.LOW)
            print('Nothing')
            time.sleep(0.1)
        
GPIO.cleanup()
        
##while True:
    ##time.sleep(0.1)


