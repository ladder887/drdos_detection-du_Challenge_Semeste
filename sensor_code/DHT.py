import RPi.GPIO as GPIO
import time
import board
import Adafruit_DHT

dht = Adafruit_DHT.DHT11
DHTpin = 2
while True:
    try:
        humidity_date, temperature_date = Adafruit_DHT.read_retry(dht, DHTpin)
        #temperature_date = dht.temperature
        #humidity_date = dht.humidity
        print('Temp : {:.1f} C    Humidity : {}%'.format(temperature_date, humidity_date))
                
    except RuntimeError as error:
        print(error.arge[0])
        time.sleep(2.0)
        continue
            
    except Exception as error:
        dht.exit()
        raise error
            
    finally:
        GPIO.cleanup()
            
    time.sleep(2)