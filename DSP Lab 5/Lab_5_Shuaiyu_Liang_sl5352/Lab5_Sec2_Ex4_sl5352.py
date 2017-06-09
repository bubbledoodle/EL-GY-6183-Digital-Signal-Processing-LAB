# play_randomly.py
"""
PyAudio Example: Generate random pulses and input them to an IIR filter of 2nd order.
It sounds like pings from a Sonar or from a Geiger Counter.
Gerald Schuller, March 2015 
Modified - Ivan Selesnick, October 2015
Modified - Shuaiyu Liang, October 2015
"""

import pyaudio
import struct
import time
from math import sin, cos, pi
import random
from myfunctions import clip16
# import numpy as np

WIDTH = 2           # Bytes per sample
CHANNELS = 1
RATE = 8000         # Sampling rate in Hz

# Parameters
T = 10      # Total play time (seconds)
Ta = 0.4    # Decay time (seconds)
f1 = 1000    # Frequency (Hz)
THRESHOLD = 2.5 / RATE          # For a rate of 2.5 impulses per second

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude

def my_callback_fun(input_string, block_size, time_info, status):
    N = block_size

    y = [0.0 for n in range(N)]  #initializing

    rand_freq = random.random()
    om1 = 2.0 * pi * float(f1 * rand_freq)/RATE

    # Filter coefficients (second-order IIR)
    a1 = -2*r*cos(om1)
    a2 = r**2
    b0 = sin(om1)

    for n in range(N):

        rand_val = random.random()
        if rand_val < THRESHOLD:
            x = 15000
        else:
            x = 0

        y[n] = b0 * x - a1 * y[n-1] - a2 * y[n-2]  
        y[n] = clip16(y[n])

    output_string = struct.pack('h' * N, *y)
    return (output_string, pyaudio.paContinue) # return data and status

# Open the audio output stream
p = pyaudio.PyAudio()

PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(format = PA_FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = False,
                output = True,
                stream_callback = my_callback_fun)

stream.start_stream()
print 'Playing for {0:f} seconds ...'.format(T),
time.sleep(T)
stream.stop_stream()
print 'Done.'

stream.close()
p.terminate()
