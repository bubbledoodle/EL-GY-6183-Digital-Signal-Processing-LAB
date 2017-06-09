import pyaudio
import struct
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal 

# audio parameters
WIDTH = 2
CHANNELS = 1
RATE = 16000
BLOCKSIZE = 1024
DURATION = 10

NumBlocks = int(DURATION * RATE / BLOCKSIZE)

print 'the number of BLOCKSIZE = ', BLOCKSIZE
print 'the sampling rate = ', RATE
print 'runing time = ', DURATION,'points...'

#other parameters
f1 = 400
n = range(0, BLOCKSIZE)
I = np.sqrt(-1+0j)
time = [float(t)/RATE for t in n]

print'real time playing'
p = pyaudio.PyAudio()
PA_format = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_format,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True)


for i in range(0, NumBlocks):
	input_string = stream.read(BLOCKSIZE)
	input_tuple = struct.unpack('h' *  BLOCKSIZE, input_string)
	input_array = np.asarray(input_tuple) #convert list
	time_array = np.asarray(time)

	#filtering
	[b_1pf, a_1pf] = signal.ellip(7, 0.2, 50, 0.48)
	n = np.array([0,1,2,3,4,5,6,7])
	s = np.exp(I * 0.5 * np.pi * n)
	b = b_1pf * s
	a = a_1pf * s
	r = signal.lfilter(b,a,input_array)
	y = r * np.exp(I * 2 * np.pi * f1 * (time_array + i * float(BLOCKSIZE/RATE)))
	y = np.real(y)

	output_block = y.tolist()
	output_string = struct.pack('h' * BLOCKSIZE, * output_block)
	stream.write(output_string)
	
print 'Done!'
stream.stop_stream()
stream.close()
p.terminate()

