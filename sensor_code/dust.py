import RPi.GPIO as GPIO
import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

spi.max_speed_hz = 500000
dustLED = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(dustLED, GPIO.OUT)


def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1,(8+adcChannel)<<4,0])
    print(buff)
    adcValue = ((buff[1]&3)<<8)+buff[2]
    return adcValue


try:
    while True:
        GPIO.output(dustLED, GPIO.LOW)
        time.sleep(0.00028)
        adcChannel = 2
        adcValue = read_spi_adc(adcChannel)
        print(adcValue)
        time.sleep(0.00004)
        GPIO.output(dustLED, GPIO.HIGH)
        time.sleep(0.00968)
        calVoltage = adcValue * (5.0 / 1024.0)
        #print(calVoltage)
        dust_date = (0.172 * calVoltage - 0.01) * 1000
        print('dust %d' %dust_date)
        time.sleep(2)

except Exception as e:
    print(e)

finally:
    spi.close()
    GPIO.cleanup()
    
        
        
            
