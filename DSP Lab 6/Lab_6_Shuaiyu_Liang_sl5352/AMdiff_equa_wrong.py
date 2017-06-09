import pyaudio
import numpy as np
import struct
from myfunctions import clip16

WIDTH = 2
CHANNELS = 1
RATE = 16000
BLOCKSIZE = 1024
DURATION = 4096

NumBlocks = (DURATION / BLOCKSIZE)

print 'the number of BLOCKSIZE = ', BLOCKSIZE
print 'the sampling rate = ', RATE
print 'runing time = ', DURATION,'points...'

#AM parameters
f0 = 400

# initializing
output_block = [0 for i in range(0,BLOCKSIZE)]
output_real_block = [0 for i in range(0,BLOCKSIZE)]
theta = 0.0
theta_del = (float(BLOCKSIZE * f0) / RATE - np.floor(BLOCKSIZE * f0 / RATE)) * 2.0 * np.pi
I = np.sqrt(-1+0j)
#filter parameter
#numerator
b0 = 0.0423
b1= 0.1193j
b2 = -0.2395
b3 = -0.3208j
b4 = 0.3208
b5 = 0.2395j
b6 = -0.1193
b7 = -0.0423j
#denominator
a0 = 1
a1 = -1.2762j
a2 = -2.6471
a3 = 2.2785j
a4 = 2.1026
a5 = -1.1252j
a6 = -0.4876
a7 = 0.1136j

print'real time playing'

p = pyaudio.PyAudio()
PA_format = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_format,
				channels = CHANNELS,
				rate = RATE,
				input = True,
				output = True)

for i in range(0,NumBlocks):
	input_string = stream.read(BLOCKSIZE)
	input_tuple = struct.unpack('h' * BLOCKSIZE, input_string)
	for n in range(0,BLOCKSIZE):

		output_block[n] = b0*input_tuple[n] + b1*input_tuple[n-1] + b2*input_tuple[n-2] + b3*input_tuple[n-3] + b4*input_tuple[n-4] + b5*input_tuple[n-5] + b6*input_tuple[n-6] + b7*input_tuple[n-7] - a1*output_block[n-1] - a2*output_block[n-2] - a3*output_block[n-3] - a4*output_block[n-4] - a5*output_block[n-5] - a6*output_block[n-6] - a7*output_block[n-7]

		output_block[n] = output_block[n] * np.exp(a * 2 * np.pi * f0 * n/RATE +theta)
		output_real_block[n] = clip16(output_block[n].real)
	theta = theta + theta_del

	output_string = struct.pack('h' * BLOCKSIZE, *output_real_block)

	stream.write(output_string)
print 'Done!'
stream.stop_stream()
stream.close()
p.terminate()