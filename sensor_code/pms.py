from pms7003 import Pms7003Sensor, PmsSensorException

sensor = Pms7003Sensor('/dev/ttyUSB0')

try:
    while True:

        Dust = sensor.read()

        print('\nStandard Condition -----------------------')
        print('PM1.0:\t', Dust['pm1_0cf1'])
        print('PM2.5:\t', Dust['pm2_5cf1'])
        print('PM10:\t', Dust['pm10cf1'])


        print('\nCurrent Condition -----------------------')
        print('PM1.0:\t', Dust['pm1_0'])
        print('PM2.5:\t', Dust['pm2_5'])
        print('PM10:\t', Dust['pm10'])
        print('\nNumber of particles in 0.1L of air-----------------------')
        print('>0.3nm:\t', Dust['n0_3'])
        print('>0.5nm:\t', Dust['n0_5'])
        print('>1.0nm:\t', Dust['n1_0'])
        print('>2.5nm:\t', Dust['n2_5'])
        print('>5.0nm:\t', Dust['n5_0'])
        print('>10nm:\t', Dust['n10'])

except PmsSensorException:
    print('Connection problem')

finally:
    sensor.close()
