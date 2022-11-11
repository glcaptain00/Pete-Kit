import smbus2 as smbus #import smbus2, but name it smbus instead
from ADCPi import ADCPi #import the ADCPi class from the ADCPi library
from time import sleep

#Set up the configurable values at the top!
#We do this here so that you can easily adjust
#These values instead of hunting for them in the code.
ADC_res = 18 #The resolution of the ADC. Options are: 18, 16, 14, 12
             #More bits means a slower sample rate, but more precise measurements
ADC_used_channel = 1 #The channel the gas sensor is attached to

#We are using channel 1 on the I2C. The Raspberry Pi has 2 channels, but the other is typically only used by the system.
I2C_Channel = 1

#The I2C addresses for the connected devices
#NOTE: These are specified by the people who made the deviice! Most devices do not let you change these!
ADC_ch1 = 0x68
ADC_ch2 = 0x69
Temp_ch = 0x38

#Create a variable to store our connection to the I2C Bus
bus = smbus.SMBus(I2C_Channel)

#Setup the messages to send
AHT20_MEASURE_START = smbus.i2c_msg.write(0x38, [0xAC, 0x33, 0x00])
AHT20_MEASURE_READ = smbus.i2c_msg.read(0x38, 7)
AHT20_MEASURE_CAL = smbus.i2c_msg.write(0x38, [0xBE])

#Setup the ADC Connection
ADC = ADCPi(ADC_ch1, ADC_ch2, ADC_res)
#Set ADC to continuous sample mode
ADC.set_conversion_mode(1)

#Tell the Temperature sensor to calibrate itself
bus.i2c_rdwr(AHT20_MEASURE_CAL)

#Start a loop that loops forever
while True:
	bus.i2c_rdwr(AHT20_MEASURE_START)
	bus.i2c_rdwr(AHT20_MEASURE_READ)

	#Take measurements
	dataRaw = AHT20_MEASURE_READ.buf[1:6]
	adcData = ADC.read_voltage(ADC_used_channel)

	#Convert bytes from I2C to integer
	data = int.from_bytes(dataRaw, "big")


	humi = ( data & 0xfffff00000 ) >> 20
	temp = ( data & 0xfffff )

	humi = humi / 0xfffff
	temp = temp / 0xfffff

	print(f"Humidity: {humi * 100}%\nTemperature: {temp * 200-50}\nLight: {adcData}")
	sleep(1)


