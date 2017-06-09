# phasor audio effect using periodically time varying all pass filter
# by Shuaiyu Liang @ 11/17/2015
# sl5352 NYU Tandon School of Engineering
import pyaudio
import struct
import wave
import math
import time
from myfunctions import clip16


RATE = 16000    # sampling rate
CHANNELS = 1    # stereo
WIDTH = 2       # bytes per sample

T = 5.0
fm = 5
W = 0.2
R = 0.8

def my_callback(input_string, block_size, time_info, status):
    global kr, kw, T, buffer_MAX
    output_block = [0 for i in range(0,block_size)] 
    input_value = struct.unpack('h' * block_size, input_string)
    for n in range(0,block_size):

        fc = fm * W ** math.sin( 2 * math.pi * fm * n / RATE )
        output_block[n] = clip16(R**2*input_value[n] - 2*R*math.cos(fc)*input_value[n-1] + input_value[n-2] + 2*R*math.cos(fc)*output_block[n-1] - R**2*output_block[n-2])
        output_block[n] = clip16(output_block[n] + input_value[n])

    # Convert output signal to binary string
    output_string = struct.pack('h' * block_size, *output_block)
    
    return (output_string, pyaudio.paContinue)

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                stream_callback = my_callback)

print('Playing!')
stream.start_stream()
time.sleep(5.0)
stream.stop_stream()
print 'Done.'

stream.close()
p.terminate()